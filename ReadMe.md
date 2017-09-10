# このソフトウェアについて

SQLite3のCreateTable文を解析・構築するツールを作った（中途半端）。

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [Python 3.4.3](https://www.python.org/downloads/release/python-343/)
* [SQLite](https://www.sqlite.org/) 3.8.2

# 問題

* 主キー制約は特定の記述しか解析できない
    * `Id integer primary key`
    * それ以外の以下のような記述は解析できない
        * `primary key(Id)`
        * `primary key(Id, Name)`
* 外部キー制約は特定の記述しか解析できない
    * `foreign key (Key) references ParentTable(ParentColumn)`
    * それ以外の以下のような記述は解析できない
        * `foreign key (Key1, Key2) references ParentTable(Column1, Column2)`
        * `Id integer references ParentTable(ParentColumn)`
        * `Id integer references ParentTable`
            * `create index Id on Parent(Column);`
        * 以下の外部キーに付与する値には未対応(https://sqlite.org/foreignkeys.html)
            * `DEFERRABLE INITIALLY DEFERRED`
            * `ON UPDATE CASCADE`
            * `ON DELETE CASCADE`

正式な構文を調査したわけではないため、他にも抜け漏れがあるかもしれない。

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

Library|License|Copyright
-------|-------|---------
[requests](http://requests-docs-ja.readthedocs.io/en/latest/)|[Apache-2.0](https://opensource.org/licenses/Apache-2.0)|[Copyright 2012 Kenneth Reitz](http://requests-docs-ja.readthedocs.io/en/latest/user/intro/#requests)
[dataset](https://dataset.readthedocs.io/en/latest/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2013, Open Knowledge Foundation, Friedrich Lindenberg, Gregor Aisch](https://github.com/pudo/dataset/blob/master/LICENSE.txt)
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright © 1996-2011 Leonard Richardson](https://pypi.python.org/pypi/beautifulsoup4),[参考](http://tdoc.info/beautifulsoup/)
[pytz](https://github.com/newvem/pytz)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2003-2005 Stuart Bishop <stuart@stuartbishop.net>](https://github.com/newvem/pytz/blob/master/LICENSE.txt)
[furl](https://github.com/gruns/furl)|[Unlicense](http://unlicense.org/)|[gruns/furl](https://github.com/gruns/furl/blob/master/LICENSE.md)
[PyYAML](https://github.com/yaml/pyyaml)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2006 Kirill Simonov](https://github.com/yaml/pyyaml/blob/master/LICENSE)

