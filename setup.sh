echo 'install mask-validator...'
# git clone https://github.com/Odin-son/mask-validator
# cd mask-validator
pip3 install -e .

cp mask_validator.png ~/.local/share/icons/mask_validator.png

chmod a+x mask_validator.desktop
cp mask_validator.desktop ~/Desktop/mask_validator.desktop
