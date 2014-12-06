


fixedip:
	sudo cp ./config/interfaces /etc/network/interfaces
	sudo cp ./config/resolv.conf /etc/resolv.conf

install:
	sudo cp ./netcharger /etc/init.d/
	sudo chmod +x /etc/init.d/netcharger
	sudo update-rc.d /etc/init.d/netcharger defaults

start:
	sudo /etc/init.d/netcharger start

stop:
	sudo /etc/init.d/netcharger stop
