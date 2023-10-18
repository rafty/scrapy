import scrapy
import pathlib


class ScrapyBooksSpiderSpider(scrapy.Spider):
    name = "scrapy_books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"]

    def parse(self, response):

        # Book pageのlinkの抽出
        book_page_links = response.xpath('//div/ol/li/article/h3/a/@href')
        yield from response.follow_all(book_page_links, self.parse_book)

        # Book list pageのnext pageへ移行
        pagenation_links = response.xpath('//div/ul/li[@class="next"]/a/@href')
        yield from response.follow_all(pagenation_links, self.parse)

    def parse_book(self, response):
        # Book Pageのスクレイピング

        # json出力
        yield {
            'title': response.xpath('//head/title/text()').get(),
            'url': response.url
        }

        # スクレイピングしたHTMLファイルをローカルディレクトリに保存
        self.save_html_file(response=response)

    def save_html_file(self, response):
        # ./scrapy_books_spider/ディレクトリ配下にHTMLファイルを保存
        file_name = self.make_path_strings(response)
        with open(file_name, 'w') as f:
            f.write(response.text)

    @staticmethod
    def make_path_strings(response) -> str:
        # VectorDBに読み込ませるHTMLのURLをディレクトリ構成に変換します。
        # 例:
        # https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.htmlを
        # ./aws_dev_docs/docs.aws.amazon.com/kendra/latest/db/what-is-kendra.htmlに変換します。

        root_path = './scrapy_books_spider'
        url = response.url

        path = url.replace('https:/', root_path)
        path_list = path.rsplit('/', 1)

        directory = path_list[0] + '/'
        file_name = path_list[1]

        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        print(f'directory_path: {directory + file_name}')
        return directory + file_name
