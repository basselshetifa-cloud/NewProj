package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "regexp"
    "strconv"
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
    
    // PARSE block fields
    Left            string `json:"left,omitempty"`
    Right           string `json:"right,omitempty"`
    Selector        string `json:"selector,omitempty"`
    JSONPath        string `json:"json_path,omitempty"`
    Pattern         string `json:"pattern,omitempty"`
    CaptureName     string `json:"capture_name,omitempty"`
    Recursive       bool   `json:"recursive,omitempty"`
    CaseSensitive   bool   `json:"case_sensitive,omitempty"`
    
    // FUNCTION block fields
    Function string `json:"function,omitempty"`
    Input    string `json:"input,omitempty"`
    Param1   string `json:"param1,omitempty"`
    Param2   string `json:"param2,omitempty"`
    SaveAs   string `json:"save_as,omitempty"`
    
    // KEYCHECK block fields
    Logic    string `json:"logic,omitempty"`
    Comparer string `json:"comparer,omitempty"`
}

type Condition struct {
    Left      string `json:"left"`
    Condition string `json:"condition"`
    Comparer  string `json:"comparer"`
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
    UseSelenium     bool              `json:"use_selenium"`
    BrowserMode     string            `json:"browser_mode"`
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
    logic := block.Logic
    if logic == "" {
        logic = "AND"
    }
    
    passCount := 0
    
    for _, cond := range block.Conditions {
        left := ReplaceVariables(cond.Left, nil, captures)
        right := ReplaceVariables(cond.Right, nil, captures)
        
        // Support both old "Condition" field and new "Comparer" field
        comparer := cond.Comparer
        if comparer == "" {
            comparer = cond.Condition
        }
        
        passed := false
        switch comparer {
        case "Exists", "EXISTS":
            passed = left != "" && left != "<nil>"
        case "DoesNotExist", "NOT_EXISTS":
            passed = left == "" || left == "<nil>"
        case "EqualTo", "EQUALS":
            passed = left == right
        case "NotEqualTo", "NOT_EQUALS":
            passed = left != right
        case "Contains", "CONTAINS":
            passed = strings.Contains(left, right)
        case "NotContains", "NOT_CONTAINS":
            passed = !strings.Contains(left, right)
        case "StartsWith", "STARTS_WITH":
            passed = strings.HasPrefix(left, right)
        case "EndsWith", "ENDS_WITH":
            passed = strings.HasSuffix(left, right)
        case "GreaterThan", "GREATER_THAN":
            leftInt, err1 := strconv.Atoi(left)
            rightInt, err2 := strconv.Atoi(right)
            if err1 == nil && err2 == nil {
                passed = leftInt > rightInt
            }
        case "LessThan", "LESS_THAN":
            leftInt, err1 := strconv.Atoi(left)
            rightInt, err2 := strconv.Atoi(right)
            if err1 == nil && err2 == nil {
                passed = leftInt < rightInt
            }
        case "MatchesRegex", "REGEX":
            re := regexp.MustCompile(right)
            passed = re.MatchString(left)
        case "LENGTH":
            passed = len(left) >= len(right)
        }
        
        if passed {
            passCount++
        }
        
        // For AND logic, if any condition fails, return failure
        if logic == "AND" && !passed {
            return block.Failure
        }
        
        // For OR logic, if any condition passes, return success
        if logic == "OR" && passed {
            return block.Success
        }
    }
    
    // For AND logic, all conditions passed
    if logic == "AND" && passCount == len(block.Conditions) {
        return block.Success
    }
    
    // For OR logic, no conditions passed
    return block.Failure
}