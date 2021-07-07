# Tạo chatbot hỗ trợ sinh viên trong quy chế đào tạo đại học Rasa framework

## Mở đầu
- Trong phần này mình sẽ mô tả từng bước cài đặt môi trường cho  mã nguồn mở Rasa.

### Những thứ bạn cần cài đặt và cách thiết lập chúng

```
python
pip
conda
rasa
underthesea
```

### Cài đặt thiết lập 
1. Cài đặt `python` phiên bản > 3.5 (https://codecute.com/python/huong-dan-cai-dat-lap-trinh-python-tren-windows-10.html)
2. Cài đặt `pip` (https://quantrimang.com/cai-dat-python-package-voi-pip-tren-windows-mac-va-linux-162623)
3. cài đặt `conda` (https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
        3.1.1 Tạo môi trường conda để đóng gói các thư viện 
        3.1.2 `conda create -n rasa python=3.8`
        3.1.3 `conda activate rasa`
4. cài đặt `underthesea` bằng `pip install underthesea` => doc (https://underthesea.readthedocs.io/en/latest/readme.html)
5. Cài đặt `rasa` bằng  `pip install rasa` => doc (https://rasa.com/docs/rasa/installation)

## Cách chạy project này
- Bạn phải cài đặt `git` trước khi thực hiện các bước bên dưới:
1. git clone  https://github.com/sangle321/CHATBOT-RASA-DHKH
2. Di chuyển đến thư mục `cd CHATBOT-RASA-DHKH`
3. `conda activate rasa`
4. `pip install -r requirements.txt`
5. `rasa run actions`
6. `rasa shell`
7. Hoàn thành các bước trên thì bạn được code của project này

## Deployment
- Cài đặt các bước deploy để test với FB (Chưa custom)

## Built With
- Rasa
- python

## Contributing
- Mọi ý kiến phản hồi hay cài chưa được vui lòng liên hệ (`sangitk41d@gmail.com`)

## Versioning
- 1.0

## Authors

* **Sang le** - *Initial work*
* **Gv. Đoan Thi Hong Phuoc** - *Initial work*


## License
This project is licensed under the MIT License ở file readme.md

* Hat tip to anyone whose code was used
* Inspiration
* etc
