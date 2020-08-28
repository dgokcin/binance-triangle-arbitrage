# binance-triangle-arbitrage
A short script for finding triangle arbitrage  opportunities in Binance
. Heavily inspired from [this](https://gist.github.com/Valian/d16ef72a0e17ee82c0acf606d6a744d7) gist.

## Usage

- You can set the primary coins by modifying primary.txt. It should look
 something like:
 ```text
XRP
OMG
BTC
BNB
USDT
ETH
```

- After adjusting your primary coins, build the container with:
```shell script
docker build -t binance .
```

- Once your container is built, mount the primary.txt as a volume for your
 container.
 ```shell script
docker run -v "$(pwd)"/primary.txt:/app/primary.txt binance
```

- The output should look something similar to:
```text
Downloaded in: 3.2185s
Computed in: 0.0379s
BTC->WAN->ETH->BTC          0.0112% <- profit!
     WAN  / BTC :    30618.49357012
     ETH  / WAN :        0.00094900
     BTC  / ETH :        0.03427000
```
