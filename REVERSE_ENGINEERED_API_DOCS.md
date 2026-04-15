# BASE URL

https://apichotadhobi.rdgroupco.com

# Endpoints
1) `/dhobi/v2/common/generateLoginOtp`

Request
```
:method: POST
:path: /dhobi/v2/common/generateLoginOtp
:authority: apichotadhobi.rdgroupco.com
:scheme: https
accept: application/json, text/plain, */*
content-type: application/json
content-length: 71
accept-encoding: gzip
user-agent: okhttp/4.9.2

{"role":"user","email_address":"<YOUR_VIT_EMAIL>"}
```

Response
```
:status: 200
access-control-allow-origin: *
alt-svc: h3=":443"; ma=2592000
content-type: application/json; charset=utf-8
date: Tue, 14 Apr 2026 12:43:57 GMT
vary: Origin
via: 1.1 Caddy
x-request-id: <Random-UUID>
content-length: 21

{"message":"Success"}
```
<hr>


2) `/dhobi/v2/common/verifyLoginOtp`

Request
```
:method: POST
:path: /dhobi/v2/common/verifyLoginOtp
:authority: apichotadhobi.rdgroupco.com
:scheme: https
accept: application/json, text/plain, */*
content-type: application/json
content-length: 72
accept-encoding: gzip
user-agent: okhttp/4.9.2

{"email_address":"<YOUR_VIT_EMAIL>","otp":"<Your otp here>"}
```

Response
```
:status: 200
access-control-allow-origin: *
alt-svc: h3=":443"; ma=2592000
content-type: application/json; charset=utf-8
date: Tue, 14 Apr 2026 12:44:13 GMT
vary: Origin
via: 1.1 Caddy
x-request-id: 295d69d8-7995-4671-bf38-aba7e4f0cc69
content-length: 453

{"token":"<JWT Token to be used as authorization header in further requests>"}
```
<hr>

3) `/dhobi/v2/common/userDetails`

Request
```
:method: GET
:path: /dhobi/v2/common/userDetails
:authority: apichotadhobi.rdgroupco.com
:scheme: https
accept: application/json, text/plain, */*
authorization: Bearer <JWT_TOKEN>
accept-encoding: gzip
user-agent: okhttp/4.9.2
```

Response
```
:status: 200
access-control-allow-origin: *
alt-svc: h3=":443"; ma=2592000
content-type: application/json; charset=utf-8
date: Tue, 14 Apr 2026 12:44:13 GMT
vary: Origin
via: 1.1 Caddy
x-request-id: 1bf239d2-688f-44ca-b33a-16985233608c
content-length: 366

{"id":"27e26f99-ddee-42a2-bb0b-a3a745722637","org_id":"<REG_NO>","email_address":"<YOUR_VIT_EMAIL>","name":"<NAME>","mobile_number":"","ctry_code":"91","block":"MHT","permitted_blocks":"MHT","role":"user","is_active":true,"created_at":"2025-09-20T15:34:18.975Z","created_by":"App admin","user_activated_at":"2025-09-20T15:34:18.975Z"}
```
<hr>

4) `/dhobi/v2/wash/washStats`

Request
```
:method: GET
:path: /dhobi/v2/wash/washStats
:authority: apichotadhobi.rdgroupco.com
:scheme: https
accept: application/json, text/plain, */*
authorization: Bearer <JWT_TOKEN>
accept-encoding: gzip
user-agent: okhttp/4.9.2
```

Response
```
:status: 200
access-control-allow-origin: *
alt-svc: h3=":443"; ma=2592000
content-type: application/json; charset=utf-8
date: Tue, 14 Apr 2026 12:44:14 GMT
vary: Origin
via: 1.1 Caddy
x-request-id: c4f0bfcc-237d-4435-9d9a-ad2a04debd45
content-length: 152

{"allotted_wash_count":35,"remaining_wash_count":15,"in_progress_wash_count":1,"valid_till":"2026-03-31","requested_wash_id":null,"clothes_per_wash":20}
```
<hr>

5) `/dhobi/v2/wash/searchWash`

Request

here the params are pagesize pagenumber washstatus feel free to change any of these as required also 
```
:method: GET
:path: /dhobi/v2/wash/searchWash?&pageSize=3&pageNumber=1&wash_status=washing,requested,completed
:authority: apichotadhobi.rdgroupco.com
:scheme: https
accept: application/json, text/plain, */*
authorization: Bearer <JWT_TOKEN>
accept-encoding: gzip
user-agent: okhttp/4.9.2
```

Response
```
:status: 200
access-control-allow-origin: *
alt-svc: h3=":443"; ma=2592000
content-encoding: gzip
content-type: application/json; charset=utf-8
date: Tue, 14 Apr 2026 12:44:15 GMT
vary: Origin
vary: Accept-Encoding
via: 1.1 Caddy
x-request-id: f71afaf7-41bd-4ccf-a24f-6b70f08191f3
content-length: 458

{"total_count":1,"data":[{"wash_id":"086e92e3-8e4e-436a-af59-d9bca2f6fc77","user_id":"27e26f99-ddee-42a2-bb0b-a3a745722637","user_org_id":"<REG_NO>","user_email_address":"<YOUR_VIT_EMAIL>","user_name":"<NAME>","wash_requested_date":"4/13/2026, 11:48:53 AM","washing_block":"MHT","tracking_number":20,"clothes_count":14,"wash_status":"washing","user_comments":"","admin_comments":"","wash_token":"Blue-1711","dispatch_instructions":"","dispatched_by_id":"","dispatched_by_email":"","dispatched_by_name":"","dispatched_at":"","received_by_id":"921b8446-c187-4f0b-b351-fec6c3193f7d","received_by_email":"CHOTMN37@gmail.com","received_by_name":"AKASH.R","received_at":"4/13/2026, 11:50:49 AM","updated_by_id":"921b8446-c187-4f0b-b351-fec6c3193f7d","updated_by_email":"CHOTMN37@gmail.com","updated_by_name":"AKASH.R","updated_at":"4/13/2026, 11:50:49 AM"}]}
```
<hr>

6) `/dhobi/v2/wash/requestWash`

Main endpoint for requesting Wash

Request
```
Method: POST
URL
/dhobi/v2/wash/requestWash
Headers
accept:
application/json, text/plain, */*
Accept-Encoding:
gzip
authorization:
Bearer <JWT_TOKEN>
Connection:
Keep-Alive
Content-Length:
40
Content-Type:
application/json
Host:
apichotadhobi.rdgroupco.com
User-Agent:
okhttp/4.9.2

{
  "clothes_count": "10",
  "user_comment": ""
}
```

Response
```
{
  "wash_id": "cc0f9659-8b73-4f98-a376-40b8438e89b5",
  "user_id": "27e26f99-ddee-42a2-bb0b-a3a745722637",
  "user_org_id": "<REG_NO>",
  "user_email_address": "<YOUR_VIT_EMAIL>",
  "user_name": "<NAME>",
  "wash_requested_date": "4/15/2026, 10:18:36 PM",
  "washing_block": "MHT",
  "tracking_number": 21,
  "clothes_count": 10,
  "wash_status": "requested",
  "user_comments": "",
  "admin_comments": "",
  "wash_token": "",
  "dispatch_instructions": "",
  "dispatched_by_id": "",
  "dispatched_by_email": "",
  "dispatched_by_name": "",
  "dispatched_at": "",
  "received_by_id": "",
  "received_by_email": "",
  "received_by_name": "",
  "received_at": "",
  "updated_by_id": "27e26f99-ddee-42a2-bb0b-a3a745722637",
  "updated_by_email": "<YOUR_VIT_EMAIL>",
  "updated_by_name": "<NAME>",
  "updated_at": "4/15/2026, 10:18:36 PM"
}
```

Qr code in all cases will be of "wash_id"
