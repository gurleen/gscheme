(define sock (socket-create))

(socket-connect sock "127.0.0.1" 65432)

(socket-send sock "hello, world!")

(define rv (socket-recieve sock 1024))

(print rv)