for i in `seq 0 60`; do
  echo `cat /proc/meminfo | grep Active: | sed 's/Active: //g'`/`cat /proc/meminfo | grep SwapFree: | sed 's/SwapFree: //g'` >> usage.txt
    sleep 1m
    done
