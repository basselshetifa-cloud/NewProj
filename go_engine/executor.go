package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "net/url"
    "time"
)

type CheckResult struct {
    Valid        bool
    Status       string
    StatusCode   int
    Captures     map[string]string
    CheckTime    float64
    ErrorMessage string
}

func ExecuteConfig(config *ServiceConfig, cookieContent string, proxyURL string) *CheckResult {
    start := time.Now()
    
    cookies, err := ParseCookies(cookieContent, config.CookieFormat)
    if err != nil {
        return &CheckResult{
            Valid:        false,
            Status:       "ERROR",
            ErrorMessage: fmt.Sprintf("Cookie parse error: %%v", err),
        }
    }
    
    client := &http.Client{
        Timeout: time.Duration(config.Timeout) * time.Second,
    }
    
    if proxyURL != "" {
        proxy, _ := url.Parse(proxyURL)
        client.Transport = &http.Transport{
            Proxy: http.ProxyURL(proxy),
        }
    }
    
    responses := make(map[string]string)
    captures := make(map[string]string)
    
    for _, block := range config.Blocks {
        switch block.Type {
        case "REQUEST":
            blockURL := ReplaceVariables(block.URL, cookies, captures)
            
            req, _ := http.NewRequest(block.Method, blockURL, nil)
            
            for k, v := range block.Headers {
                headerValue := ReplaceVariables(v, cookies, captures)
                req.Header.Set(k, headerValue)
            }
            
            resp, err := client.Do(req)
            if err != nil {
                return &CheckResult{
                    Valid:        false,
                    Status:       "ERROR",
                    ErrorMessage: fmt.Sprintf("Request failed: %%v", err),
                    CheckTime:    time.Since(start).Seconds(),
                }
            }
            
            body, _ := ioutil.ReadAll(resp.Body)
            resp.Body.Close()
            
            if block.SaveResponse != "" {
                responses[block.SaveResponse] = string(body)
            }
            
        case "PARSE":
            source := responses[block.Source]
            parsed := ParseResponse(source, block.ParseType, block.Captures)
            
            for k, v := range parsed {
                captures[k] = v
            }
            
        case "KEYCHECK", "KEY CHECK":
            status := EvaluateKeyCheck(block, captures)
            return &CheckResult{
                Valid:     status == "HIT",
                Status:    status,
                Captures:  captures,
                CheckTime: time.Since(start).Seconds(),
            }
        }
    }
    
    return &CheckResult{
        Valid:     false,
        Status:    "NO_KEYCHECK",
        Captures:  captures,
        CheckTime: time.Since(start).Seconds(),
    }
}