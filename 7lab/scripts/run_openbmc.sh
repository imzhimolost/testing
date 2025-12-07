#!/bin/bash

echo "Запуск QEMU OpenBMC..."
echo "   Доступ по: https://localhost:2443 (SSH: -p 2222)"

IMAGE_NAME="obmc-phosphor-image-romulus-20250910091641.static.mtd"

if [ -f "/opt/romulus/$IMAGE_NAME" ]; then
    IMAGE="/opt/romulus/$IMAGE_NAME"
else
    IMAGE="/home/ksesha/romulus/$IMAGE_NAME"
fi

nohup qemu-system-arm \
  -m 256 \
  -M romulus-bmc \
  -nographic \
  -drive file="$IMAGE",format=raw,if=mtd \
  -net nic \
  -net user,hostfwd=tcp::2222-:22,hostfwd=tcp::2443-:443,hostfwd=udp::2623-:623,hostname=qemu \
  > qemu.log 2>&1 &

SERVER_PID=$!
echo $SERVER_PID > /tmp/qemu.pid

echo "Ожидание готовности OpenBMC..."

MAX_RETRIES=60
count=0

while [ $count -lt $MAX_RETRIES ]; do
    if curl -k -f -u root:0penBmc -s https://localhost:2443/redfish/v1 > /dev/null; then
        echo "OpenBMC (QEMU) готов!"
        exit 0
    fi
    echo -n "."
    sleep 5
    count=$((count+1))
done

echo ""
echo "Не удалось дождаться запуска QEMU."
kill $SERVER_PID 2>/dev/null || true
exit 1
