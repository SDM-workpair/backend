# backend


## Google sso 後端測試:
1. 前往 http://localhost:8000/test-google-sso 按google button
2. 去 http://localhost:8000/docs 操作 get user profile和 update user profile
3. http://localhost:8000/api/v1/users/logout 登出
4. 再操作 get user profile or update user profile 都會跳錯誤 錯誤訊息 "Could not validate credentials."

## Database 更動
1. User: password欄位改nullable
         加 is_google_sso欄位
## Database 更動細節與待討論事項
1. 所有的 id 皆改為 uuid
2. BindUser: room_uuid 是否刪除
3. User: self_tag_list, find_tag_list 移至 MR_Member_Tag Table
         liked_uset_list, hated_user_list 移至 MR_Liked_Hated_Member Table
         rcm_user_list 移至 MR_Rcmed_Member Table
4. MatchingEvent: matching_algo 用 String 存, Default = “random” -> 討論此欄位是否要存在 DB 中
5. Group: name 未設定 default
6. MachingRoom: 刪除matching_event_uuid


