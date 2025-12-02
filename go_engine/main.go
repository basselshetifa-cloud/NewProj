package main

import (
    "context"
    "encoding/json"
    "log"
    "net"

    pb "cookie_checker/proto"
    "google.golang.org/grpc"
)

type server struct {
    pb.UnimplementedCookieCheckerServer
}

func (s *server) CheckCookie(ctx context.Context, req *pb.CookieRequest) (*pb.CookieResponse, error) {
    if req.UseStealth {
        return &pb.CookieResponse{
            Service:  req.Service,
            FilePath: req.FilePath,
            Valid:    false,
            Message:  "USE_PYTHON_STEALTH",
        }, nil
    }
    
    config, err := LoadConfig(req.Service)
    if err != nil {
        return &pb.CookieResponse{
            Service:  req.Service,
            FilePath: req.FilePath,
            Valid:    false,
            Message:  fmt.Sprintf("Config error: %%v", err),
        }, nil
    }
    
    result := ExecuteConfig(config, req.Cookies, req.Proxy)
    
    capturesJSON, _ := json.Marshal(result.Captures)
    
    return &pb.CookieResponse{
        Service:       req.Service,
        FilePath:      req.FilePath,
        Valid:         result.Valid,
        StatusCode:    int32(result.StatusCode),
        Message:       result.Status,
        CheckTime:     result.CheckTime,
        ExtractedData: string(capturesJSON),
    }, nil
}

func (s *server) CheckBatch(req *pb.BatchRequest, stream pb.CookieChecker_CheckBatchServer) error {
    for _, r := range req.Requests {
        resp, _ := s.CheckCookie(context.Background(), r)
        if err := stream.Send(resp); err != nil {
            return err
        }
    }
    return nil
}

func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("Failed to listen: %%v", err)
    }

    s := grpc.NewServer()
    pb.RegisterCookieCheckerServer(s, &server{})

    log.Println("🚀 Go gRPC Server running on :50051")
    if err := s.Serve(lis); err != nil {
        log.Fatalf("Failed to serve: %%v", err)
    }
}