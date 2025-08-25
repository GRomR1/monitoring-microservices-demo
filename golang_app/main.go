package main

import (
	"encoding/json"
	"log"
	"net/http"
)

// album represents data about a record album.
type album struct {
	ID     string  `json:"id"`
	Title  string  `json:"title"`
	Artist string  `json:"artist"`
	Price  float64 `json:"price"`
}

// albums slice to seed record album data.
var albums = []album{
	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}

func main() {
	http.HandleFunc("/albums", func(w http.ResponseWriter, r *http.Request) {
		log.Println("New request /albums")
		log.Println("  Request Headers:")
		for name, values := range r.Header {
			for _, value := range values {
				log.Printf("  - %s: %s\n", name, value)
			}
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(albums)
	})

	port := ":8080"
	log.Println("Server is running on port" + port)
	log.Fatal(http.ListenAndServe(port, nil))
}
