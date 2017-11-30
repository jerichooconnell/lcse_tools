package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

func videoInfo(filename string) (float64, float64) {

	var fps float64
	var length float64

	cmd := exec.Command("mplayer", "-identify", "-frames", "0", filename)

	out, err := cmd.Output()

	if err != nil {
		log.Fatal(err)
	}

	out_str := string(out)

	for _, v := range strings.Split(out_str, "\n") {

		if strings.HasPrefix(v, "ID_VIDEO_FPS") {
			fps, _ = strconv.ParseFloat(strings.Split(v, "=")[1], 64)
		} else if strings.HasPrefix(v, "ID_LENGTH") {
			length, _ = strconv.ParseFloat(strings.Split(v, "=")[1], 64)
		}
	}

	return fps, length
}

func launchSlave(filename string, port int, screen int) *exec.Cmd {

	fmt.Println("Launching slave", filename, strconv.FormatInt(int64(port), 10))

	cmd := exec.Command("mplayer", "-fs", "-udp-slave", "-udp-seek-threshold", "2.0", "-cache", "32768", "-cache-min", "80", "-lavdopts", "threads=4",
		"-loop", "0", "-vo", "xv", "-udp-port", strconv.FormatInt(int64(port), 10),
		"-xineramascreen", strconv.FormatInt(int64(screen), 10), filename)

	//out, err := cmd.Output()
	//fmt.Println(out)
	err := cmd.Start()
	//err := cmd.Run()

	if err != nil {
		log.Fatal(err)
	}

	return cmd
}

func main() {

	flag.Parse()

	if len(flag.Args()) == 0 {
		flag.Usage()
		os.Exit(1)

	}

	filenames := flag.Args()
	fmt.Println(filenames)
	fmt.Println(len(filenames))

	slave_ct := len(filenames)

	var conn_out [10]*net.UDPConn
	fps, length := videoInfo(filenames[0])

	fmt.Println("Length ", length)
	fmt.Println("fps ", fps)

	//

	local_addr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")

	if err != nil {
		log.Fatal(err)
	}

	local_ip := net.ParseIP("127.0.0.1")

	for i := 0; i < slave_ct; i++ {
		port := 10000 + i

		// Launch slave session
		launchSlave(filenames[i], port, i)

		// Create "connection"
		addr := net.UDPAddr{Port: port, IP: local_ip, Zone: ""}

		conn_out[i], err = net.DialUDP("udp", local_addr, &addr)
		defer conn_out[i].Close()

		if err != nil {
			log.Fatal(err)
		}

	}

	tick := 1.0 / (1.0 * fps)
	fmt.Println(tick)

	time.Sleep(2000 * time.Millisecond)

	tick_time := time.Duration(1e9 * tick)

	fmt.Println("tick_time ", tick_time)

	ticker := time.NewTicker(tick_time)

	t0 := time.Now()

	for {
		//	t1 := time.Now()

		k := <-ticker.C
		var t_ms float64

		t_ms = float64(k.Sub(t0)) / 1e9

		if t_ms > length {
			t0 = time.Now()
			t_ms = 0
		}

		t_ms_str := strconv.FormatFloat(t_ms, 'f', 5, 64)

		for i := 0; i < slave_ct; i++ {
			_, err = conn_out[i].Write([]byte(t_ms_str))
			if err != nil {
				break
			}
		}

		fmt.Println(t_ms_str)

		if err != nil {
			fmt.Println("Error: ", err)
			break
		}
		//		fmt.Println("Sent", string(buf[0:n]), "from", addr, "time", t1.Sub(t0))
		//	return

	}

	for i := 0; i < slave_ct; i++ {
		_, err = conn_out[i].Write([]byte("bye"))
	}

}
