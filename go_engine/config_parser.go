package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "regexp"
    "strings"
)

type Block struct {
    ID           string            `json:"id"`
    Type         string            `json:"type"`
    URL          string            `json:"url,omitempty"`
    Method       string            `json:"method,omitempty"`
    Headers      map[string]string `json:"headers,omitempty"`
    Body         string            `json:"body,omitempty"`
    SaveResponse string            `json:"save_response,omitempty"`
    Source       string            `json:"source,omitempty"`
    ParseType    string            `json:"parse_type,omitempty"`
    Captures     map[string]string `json:"captures,omitempty"`
    Conditions   []Condition       `json:"conditions,omitempty"`
    Success      string            `json:"success,omitempty"`
    Failure      string            `json:"failure,omitempty"`
}

type Condition struct {
    Left      string `json:"left"`
    Condition string `json:"condition"`
    Right     string `json:"right"`
}

type ServiceConfig struct {
    Name            string            `json:"name"`
    Author          string            `json:"author"`
    Version         string            `json:"version"`
    URL             string            `json:"url"`
    Method          string            `json:"method"`
    CookieFormat    string            `json:"cookie_format"`
    CookieLocation  string            `json:"cookie_location"`
    Blocks          []Block           `json:"blocks"`
    SuccessKeywords []string          `json:"success_keywords"`
    FailureKeywords []string          `json:"failure_keywords"`
    RetryKeywords   []string          `json:"retry_keywords"`
    NeedsStealth    bool              `json:"needs_stealth"`
    UseProxy        bool              `json:"use_proxy"`
    Timeout         int               `json:"timeout"`
}

func LoadConfig(service string) (*ServiceConfig, error) {
    data, err := ioutil.ReadFile(fmt.Sprintf("../configs/%s.json", strings.ToLower(service)))
    if err != nil {
        return nil, err
    }
    var config ServiceConfig
    err = json.Unmarshal(data, &config)
    return &config, err
}

func ReplaceVariables(text string, cookies map[string]interface{}, captures map[string]string) string {
    re := regexp.MustCompile(`<COOKIE:([^>]+)>`)
    text = re.ReplaceAllStringFunc(text, func(match string) string {
        key := re.FindStringSubmatch(match)[1]
        if val, ok := cookies[key]; ok {
            return fmt.Sprintf("%v", val)
        }
        return ""
    })
    
    if strings.Contains(text, "<COOKIES_RAW>") {
        raw := BuildCookieString(cookies)
        text = strings.ReplaceAll(text, "<COOKIES_RAW>", raw)
    }
    
    for key, val := range captures {
        text = strings.ReplaceAll(text, fmt.Sprintf("<%s>", key), val)
    }
    
    return text
}

func BuildCookieString(cookies map[string]interface{}) string {
    var parts []string
    for k, v := range cookies {
        parts = append(parts, fmt.Sprintf("%s=%v", k, v))
    }
    return strings.Join(parts, "; ")
}

func ParseCookies(cookieContent string, format string) (map[string]interface{}, error) {
    result := make(map[string]interface{})
    
    switch format {
    case "json":
        var jsonCookies map[string]interface{}
        if err := json.Unmarshal([]byte(cookieContent), &jsonCookies); err == nil {
            return jsonCookies, nil
        }
        
    case "netscape":
        lines := strings.Split(cookieContent, "\n")
        for _, line := range lines {
            if strings.HasPrefix(line, "#") || strings.TrimSpace(line) == "" {
                continue
            }
            parts := strings.Split(line, "\t")
            if len(parts) >= 7 {
                result[parts[5]] = parts[6]
            }
        }
        
    case "header":
        pairs := strings.Split(cookieContent, ";")
        for _, pair := range pairs {
            kv := strings.SplitN(strings.TrimSpace(pair), "=", 2)
            if len(kv) == 2 {
                result[kv[0]] = kv[1]
            }
        }
        
    default:
        if strings.HasPrefix(strings.TrimSpace(cookieContent), "{") {
            return ParseCookies(cookieContent, "json")
        } else if strings.Contains(cookieContent, "\t") {
            return ParseCookies(cookieContent, "netscape")
        } else {
            return ParseCookies(cookieContent, "header")
        }
    }
    
    return result, nil
}

func ParseResponse(response string, parseType string, captures map[string]string) map[string]string {
    result := make(map[string]string)
    
    switch parseType {
    case "json":
        var data map[string]interface{}
        json.Unmarshal([]byte(response), &data)
        for key, path := range captures {
            val := GetJSONPath(data, path)
            result[key] = fmt.Sprintf("%v", val)
        }
        
    case "regex":
        for key, pattern := range captures {
            re := regexp.MustCompile(pattern)
            matches := re.FindStringSubmatch(response)
            if len(matches) > 1 {
                result[key] = matches[1]
            }
        }
    }
    
    return result
}

func GetJSONPath(data map[string]interface{}, path string) interface{} {
    path = strings.TrimPrefix(path, "$.")
    keys := strings.Split(path, ".")
    
    var current interface{} = data
    for _, key := range keys {
        if m, ok := current.(map[string]interface{}); ok {
            current = m[key]
        } else {
            return nil
        }
    }
    return current
}

func EvaluateKeyCheck(block Block, captures map[string]string) string {
    for _, cond := range block.Conditions {
        left := ReplaceVariables(cond.Left, nil, captures)
        right := cond.Right
        
        passed := false
        switch cond.Condition {
        case "EXISTS":
            passed = left != "" && left != "<nil>"
        case "CONTAINS":
            passed = strings.Contains(left, right)
        case "NOT_CONTAINS":
            passed = !strings.Contains(left, right)
        case "EQUALS":
            passed = left == right
        case "LENGTH":
            passed = len(left) >= len(right)
        }
        
        if !passed {
            return block.Failure
        }
    }
    return block.Success
}