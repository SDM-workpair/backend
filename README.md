# backend
# test

## Google sso 後端測試:
1. 前往 http://localhost:8000/test-google-sso 按google button
2. 如果是未登入過的 google 帳號，會在Database建一個新帳號
3. 在 http://localhost:8000/docs ，API旁邊有一個鎖符號的話表示需要驗證 user，點鎖後username輸入剛剛的google email，密碼隨便輸入就可以登入
4. 登入後， ex: read user me, update user profile之類的 API 就可以使用，登出後再打 API 會出現 401 error

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


