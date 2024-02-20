package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {

	b, err := os.ReadFile("russian.txt") // just pass the file name
	if err != nil {
		fmt.Print(err)
	} // convert content to a 'string'
	a, err := os.ReadFile("english.txt") // just pass the file name
	if err != nil {
		fmt.Print(err)
	}

	str_rus := string(b) // convert content to a 'string'
	str_eng := string(a)

	russian := strings.Split(str_rus, ",")
	english := strings.Split(str_eng, ",")
	fmt.Println(len(russian), " ", len(english))
	// data := make(map[string]string)
	f, _ := os.Create("result.json")

	// Create a writer
	w := bufio.NewWriter(f)
	w.WriteString("[")

	for i := 0; i < len(russian); i++ {

		w.WriteString("\n")

		w.WriteString("{" + "'" + russian[i] + "'" + ":" + "'" + english[i] + "'" + "},")

	}

	w.WriteString("]")
	fmt.Println("writed")
}
