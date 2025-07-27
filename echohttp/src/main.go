package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

type Response struct {
	Method  string      `json:"method,omitempty"`
	Path    string      `json:"path,omitempty"`
	Query   interface{} `json:"query,omitempty"`
	Headers interface{} `json:"headers,omitempty"`
	Body    string      `json:"body,omitempty"`
}

func mustRespond(w http.ResponseWriter, response *Response) {
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	responseBytes, err := json.MarshalIndent(response, "", "  ")
	if err != nil {
		panic(err)
	}
	w.Write(responseBytes)
}

func debugHandler(w http.ResponseWriter, r *http.Request) {
	body, _ := ioutil.ReadAll(r.Body)
	defer r.Body.Close()

	response := &Response{
		Method: r.Method,
		Path:   r.URL.Path,
		Body:   string(body),
	}

	if len(r.URL.Query()) > 0 {
		response.Query = r.URL.Query()
	}

	if len(r.Header) > 0 {
		response.Headers = r.Header
	}

	mustRespond(w, response)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "5000"
	}
	r := mux.NewRouter()
	r.HandleFunc("/{any:.*}", debugHandler)
	log.Println("listening on port", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
