# 日次更新の手順

対象は関東（東京・神奈川・埼玉・千葉・茨城・栃木・群馬）、甲信越（山梨・長野・新潟）、南東北（宮城・山形・福島）。端末の現在地は扱わず、公開イベント情報だけを収集します。

1. 日本時間の実行日を確認し、`events.json` と `sources.json` を取得する。
2. 既存の開催予定イベントを公式・主催者ページで再確認する。中止・延期・終了、申込条件、開催日の除外日、時刻を確認する。
3. `sources.json` を入口に、各都県について今日から60日以内のお祭り、マルシェ、展示、音楽、体験などを検索する。ふらっとろーかるだけに限定しない。情報源のアクセス制限・利用条件を尊重し、アクセス不能や再利用不可の情報は回避・転載しない。
4. 開催年が明確な公式情報を優先し、過去年の類例から今年の日程を推測しない。同じ催しは日付・会場・公式URLで重複排除する。
5. 緯度・経度は公式地図や検証可能な公開会場情報で確認する。根拠URLを `coordinate_source_url` に記録する。不明なら両方を `null`、`coordinate_status` を `unverified` にする。市役所など別の場所の座標で代用しない。
6. 画像や本文をコピーしない。概要は事実に基づく自作の短文とし、元ページへのリンクを記載する。イベントの `checked_on` はそのレコードの開催情報を実際に再確認した日とする。確認不能なら前回の日付を維持する。
7. 当日の確認結果を `generated_on` に、実際に掲載できた地域を `coverage_label` に書く。目標範囲を確認済み範囲と偽らず、`coverage_note` で未網羅と明示する。
8. `holiday_dates` は検索期間に必要な日本の祝日・振替休日を内閣府の公開情報で確認し、`holiday_source_url` を保持する。
9. `validate_feed.py events.json` 相当の検証を通す。ファイル全体は2MiB以下、イベントは3000件以下。位置情報、個人の移動履歴、秘密鍵・トークンなどは含めない。
10. GitHubの `yukilo-jp/nearby-events` の `main` に `events.json` を更新する。既存ファイルを取得し、現在のSHAを使って上書きする。書き込みが承認待ち・権限エラーになったら回避せず、状況を報告する。
11. 書き込み後に再取得し、JSONと件数・日付を検証する。HTTP取得が失敗したときは前回の配信を壊さない。`data/feed-status.json` に実際の確認日と掲載地域・件数、失敗した情報源を記録する。全件を確認できなかった場合は `partial` とする。

## JSON形式

トップレベル: `schema_version: 1`, `generated_on: yyyy-MM-dd`, `target_regions`, `coverage_label`, `coverage_note`, `holiday_dates`, `holiday_source_url`, `events`。

イベント必須: `id`, `title`, `start_date`, `end_date`, `source_name`, `source_url`, `checked_on`。

イベント任意: `start_time`/`end_time`（HH:mm、不明はnullまたは空文字）, `prefecture`, `municipality`, `venue`, `address`, `latitude`, `longitude`, `coordinate_status`, `coordinate_source_url`, `summary`, `official_url`, `discovery_url`, `cancelled`（boolean）, `excluded_dates`（休催日などのISO日付配列）。

座標は数値の緯度経度ペア。未確認はnull。`source_url` と `official_url` はhttpまたはhttps。日付範囲は両端を含みます。連日開催でないものは個々の開催日でレコードを分けるか、`excluded_dates` を明記します。日付をまたぐ催しで、終了時刻が開始時刻より早いものは日ごとに分割して正しく記載します。
