# CO2 濃度測定
* Raspberry pi に繋いだセンサから CO2 濃度取得
* OLED に出力

## 使い方メモ
* `/root`に配置する
  * `/root/DisplayCO2`
* `crontab cron.conf`
  * cron で定期実行
* systemd に登録して実行

```
cat /etc/systemd/system/display_co2.service
[Unit]
Description = Display CO2 daemon

[Service]
User = root
ExecStart = {display_co2.py へのパス}
Restart = always
Type = simple

[Install]
WantedBy = multi-user.target
```
