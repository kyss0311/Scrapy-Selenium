/*creat*/
CREATE TABLE IF NOT EXISTS article( 
	id SERIAL NOT NULL, 
	article_id TEXT PRIMARY KEY, 
	push INT, 
	title TEXT, 
	"link" TEXT, 
	author TEXT, 
	published_date TEXT, /*ex: 5/26*/ 
	"content" TEXT  
);

/*insert*/
INSERT INTO article(
	article_id, 
	push,  
	title,  
	"link",  
	author,  
	published_date, 
	"content"
)VALUES(
	'M.1737606405.A.3C9', 
	17, 
	'[討論] 壯世代學哪個語言比較有產值？', 
	'https://www.ptt.cc/bbs/Soft_Job/M.1737606405.A.3C9.html', 
	'B0988698088', 
	'1/23',
	'TEST'
);

/*select*/
SELECT * FROM article;
SELECT * FROM "comment";

/*delete*/
DELETE FROM article WHERE article_id='M.1737606405.A.3C9';

/*drop*/
DROP TABLE IF EXISTS article, "comment";

/* inner join */
SELECT article.article_id, article.title, article.link, article.published_date, "comment".push_tag,
	"comment".push_user_id, "comment".push_content, "comment".push_ipdatetime
FROM "comment"
INNER JOIN article ON article.article_id="comment".article_id
ORDER BY article.id;