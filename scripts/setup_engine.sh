# !/bin/bash

pip install -r requirements.txt

mkdir engine
cd engine

# Windows
wget https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-windows-x86-64-avx2.zip
unzip stockfish-windows-x86-64-avx2.zip
mv stockfish stockfish_win
rm stockfish-windows-x86-64-avx2.zip

mkdir lc0_win
wget https://github.com/LeelaChessZero/lc0/releases/download/v0.30.0/lc0-v0.30.0-windows-gpu-nvidia-cuda.zip
unzip lc0-v0.30.0-windows-gpu-nvidia-cuda.zip -d lc0_win
rm lc0-v0.30.0-windows-gpu-nvidia-cuda.zip

# Linux
wget https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-ubuntu-x86-64-avx2.tar
tar -xvf stockfish-ubuntu-x86-64-avx2.tar
rm stockfish-ubuntu-x86-64-avx2.tar

git clone https://github.com/LeelaChessZero/lc0.git lc0_src
chmod +x ./lc0_src/build.sh
./lc0_src/build.sh
mv ./lc0_src/build/release lc0
rm -rf lc0_src

get_models() {
    target=$1
    filename=$(basename $target)
    wget $target
    gunzip $filename
}
# Share
mkdir lc0_model
get_models https://huggingface.co/Mai0313/Lc0-Chess-Model/resolve/main/t1-512x15x8h-distilled-swa-3395000.pb.gz &
get_models https://huggingface.co/Mai0313/Lc0-Chess-Model/resolve/main/t1-256x10-distilled-swa-2432500.pb.gz &
get_models https://huggingface.co/Mai0313/Lc0-Chess-Model/resolve/main/t2-768x15x24h-swa-5230000.pb.gz
mv *.pb lc0_model
