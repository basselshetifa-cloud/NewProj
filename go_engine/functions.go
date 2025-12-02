package main

import (
	"crypto/hmac"
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/sha512"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"html"
	"math/rand"
	"net/url"
	"strconv"
	"strings"
	"time"
)

// ExecuteFunction executes a function on input data
func ExecuteFunction(funcName, input, param1, param2 string) (string, error) {
	switch {
	// Hash functions
	case funcName == "Hash-MD5":
		return HashMD5(input), nil
	case funcName == "Hash-SHA1":
		return HashSHA1(input), nil
	case funcName == "Hash-SHA256":
		return HashSHA256(input), nil
	case funcName == "Hash-SHA384":
		return HashSHA384(input), nil
	case funcName == "Hash-SHA512":
		return HashSHA512(input), nil
	case funcName == "HMAC":
		return HMAC(input, param1), nil
		
	// Encoding functions
	case funcName == "Base64-Encode":
		return Base64Encode(input), nil
	case funcName == "Base64-Decode":
		return Base64Decode(input)
	case funcName == "URLEncode":
		return url.QueryEscape(input), nil
	case funcName == "URLDecode":
		return url.QueryUnescape(input)
	case funcName == "HTMLEntityEncode":
		return html.EscapeString(input), nil
	case funcName == "HTMLEntityDecode":
		return html.UnescapeString(input), nil
		
	// String manipulation
	case funcName == "Replace":
		return strings.ReplaceAll(input, param1, param2), nil
	case funcName == "Substring":
		return Substring(input, param1, param2)
	case funcName == "CharAt":
		return CharAt(input, param1)
	case funcName == "CountOccurrences":
		return strconv.Itoa(strings.Count(input, param1)), nil
	case funcName == "Length":
		return strconv.Itoa(len(input)), nil
	case funcName == "Uppercase":
		return strings.ToUpper(input), nil
	case funcName == "Lowercase":
		return strings.ToLower(input), nil
	case funcName == "Reverse":
		return ReverseString(input), nil
	case funcName == "Trim":
		return strings.TrimSpace(input), nil
		
	// Random functions
	case funcName == "RandomNum":
		return RandomNum(param1, param2)
	case funcName == "RandomString":
		return RandomString(param1)
		
	// Time functions
	case funcName == "CurrentUnixTime":
		return strconv.FormatInt(time.Now().Unix(), 10), nil
	case funcName == "UnixTimeToDate":
		return UnixTimeToDate(input)
	case funcName == "DateToUnixTime":
		return DateToUnixTime(input)
		
	default:
		return "", fmt.Errorf("unknown function: %s", funcName)
	}
}

// Hash functions
func HashMD5(input string) string {
	hash := md5.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}

func HashSHA1(input string) string {
	hash := sha1.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}

func HashSHA256(input string) string {
	hash := sha256.Sum256([]byte(input))
	return hex.EncodeToString(hash[:])
}

func HashSHA384(input string) string {
	hash := sha512.Sum384([]byte(input))
	return hex.EncodeToString(hash[:])
}

func HashSHA512(input string) string {
	hash := sha512.Sum512([]byte(input))
	return hex.EncodeToString(hash[:])
}

func HMAC(input, key string) string {
	h := hmac.New(sha256.New, []byte(key))
	h.Write([]byte(input))
	return hex.EncodeToString(h.Sum(nil))
}

// Encoding functions
func Base64Encode(input string) string {
	return base64.StdEncoding.EncodeToString([]byte(input))
}

func Base64Decode(input string) (string, error) {
	decoded, err := base64.StdEncoding.DecodeString(input)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

// String manipulation functions
func Substring(input, start, length string) (string, error) {
	startIdx, err := strconv.Atoi(start)
	if err != nil {
		return "", err
	}
	
	if startIdx < 0 || startIdx >= len(input) {
		return "", fmt.Errorf("start index out of range")
	}
	
	if length == "" {
		return input[startIdx:], nil
	}
	
	lengthVal, err := strconv.Atoi(length)
	if err != nil {
		return "", err
	}
	
	endIdx := startIdx + lengthVal
	if endIdx > len(input) {
		endIdx = len(input)
	}
	
	return input[startIdx:endIdx], nil
}

func CharAt(input, index string) (string, error) {
	idx, err := strconv.Atoi(index)
	if err != nil {
		return "", err
	}
	
	if idx < 0 || idx >= len(input) {
		return "", fmt.Errorf("index out of range")
	}
	
	return string(input[idx]), nil
}

func ReverseString(input string) string {
	runes := []rune(input)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// Random functions
func RandomNum(min, max string) (string, error) {
	minVal, err := strconv.Atoi(min)
	if err != nil {
		return "", err
	}
	
	maxVal, err := strconv.Atoi(max)
	if err != nil {
		return "", err
	}
	
	if minVal > maxVal {
		minVal, maxVal = maxVal, minVal
	}
	
	rand.Seed(time.Now().UnixNano())
	num := rand.Intn(maxVal-minVal+1) + minVal
	return strconv.Itoa(num), nil
}

func RandomString(length string) (string, error) {
	lengthVal, err := strconv.Atoi(length)
	if err != nil {
		return "", err
	}
	
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	rand.Seed(time.Now().UnixNano())
	
	result := make([]byte, lengthVal)
	for i := range result {
		result[i] = charset[rand.Intn(len(charset))]
	}
	
	return string(result), nil
}

// Time functions
func UnixTimeToDate(timestamp string) (string, error) {
	ts, err := strconv.ParseInt(timestamp, 10, 64)
	if err != nil {
		return "", err
	}
	
	t := time.Unix(ts, 0)
	return t.Format("2006-01-02 15:04:05"), nil
}

func DateToUnixTime(dateStr string) (string, error) {
	// Try common formats
	formats := []string{
		"2006-01-02 15:04:05",
		"2006-01-02",
		"01/02/2006",
		time.RFC3339,
	}
	
	for _, format := range formats {
		t, err := time.Parse(format, dateStr)
		if err == nil {
			return strconv.FormatInt(t.Unix(), 10), nil
		}
	}
	
	return "", fmt.Errorf("unable to parse date: %s", dateStr)
}

// ParseLR parses using Left-Right method
func ParseLR(input, left, right string, caseSensitive bool) (string, error) {
	searchInput := input
	searchLeft := left
	searchRight := right
	
	if !caseSensitive {
		searchInput = strings.ToLower(input)
		searchLeft = strings.ToLower(left)
		searchRight = strings.ToLower(right)
	}
	
	// Find left boundary
	leftIdx := strings.Index(searchInput, searchLeft)
	if leftIdx == -1 {
		return "", fmt.Errorf("left boundary not found")
	}
	
	// Start searching after left boundary
	startIdx := leftIdx + len(searchLeft)
	
	// Find right boundary
	rightIdx := strings.Index(searchInput[startIdx:], searchRight)
	if rightIdx == -1 {
		return "", fmt.Errorf("right boundary not found")
	}
	
	// Extract the actual text (preserve original case)
	endIdx := startIdx + rightIdx
	return input[startIdx:endIdx], nil
}

// ParseLRRecursive parses all matches using Left-Right method
func ParseLRRecursive(input, left, right string, caseSensitive bool) []string {
	var results []string
	remaining := input
	
	for {
		result, err := ParseLR(remaining, left, right, caseSensitive)
		if err != nil {
			break
		}
		
		results = append(results, result)
		
		// Find where we stopped and continue from there
		searchStr := remaining
		if !caseSensitive {
			searchStr = strings.ToLower(remaining)
		}
		
		leftIdx := strings.Index(searchStr, strings.ToLower(left))
		if leftIdx == -1 {
			break
		}
		
		startIdx := leftIdx + len(left)
		rightIdx := strings.Index(searchStr[startIdx:], strings.ToLower(right))
		if rightIdx == -1 {
			break
		}
		
		// Continue from after this match
		remaining = remaining[startIdx+rightIdx+len(right):]
	}
	
	return results
}
