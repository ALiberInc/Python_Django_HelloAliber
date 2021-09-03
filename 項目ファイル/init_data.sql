-- ユーザーログイン accounts_customuser
-- スーパーユーザーの作成：1アカウント作成
-- パスワードuser
INSERT INTO accounts_customuser VALUES (0,'pbkdf2_sha256$216000$cG5zXkBGzPV9$4yqn2epffljnvlL2WB59SzNxFgbgA5kJfPPtTSyJ2mc=','2020/10/10 01:01:01',True,'super','ユーザー','スーパー','super@aliber.co.jp',True,True,'2020/10/10 01:01:01');


-- allauthのテーブル account_emailaddress
-- スーパーユーザーの作成：2メールアドレス認証
INSERT INTO account_emailaddress VALUES (0,'super@aliber.co.jp',True,True,0);


-- 部門 profile_app_department
-- デフォルト部門を登録する
INSERT INTO e_department VALUES 
(0,'部門無し',now(),0,now(),0,now(),0),
(1,'営業部',now(),0,now(),0,now(),0),
(2,'総務・経理部',now(),0,now(),0,now(),0),
(3,'システム開発部',now(),0,now(),0,now(),0);


-- 社員情報 profile_app_profile
-- スーパーユーザーの作成：3プロフィールを登録する
INSERT INTO e_profile VALUES (
    0,0,'スーパー','ユーザー','スーパー','ユーザー',0,'19921010',
    '中国','08012345678','1710001','住所A','住所B','ABCDE','1234567',2,
    'e11','e12','113','e21','e22','123','e31','e32','133',
    0,now(),0,now(),0
    );

