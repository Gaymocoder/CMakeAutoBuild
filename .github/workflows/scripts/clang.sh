wget https://apt.llvm.org/llvm.sh
chmod +x llvm.sh
sudo ./llvm.sh 22
sudo apt update
sudo apt install -y libc++-22-dev libc++abi-22-dev

sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-22 100
sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-22 100