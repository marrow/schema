h1(#title). Marrow Schema

bq(subtitle). A declarative, universal declarative schema architecture.

bq(byline). (C) 2013, Alice Bevan-McGregor and contributors.

bq(byline). "https://github.com/marrow/marrow.schema":github-project

[github-project]https://github.com/marrow/marrow.schema



h2(#what-is). %1.% What is Marrow Schema?




h2(#installation). %2.% Installation

Installing @marrow.schema@ is easy, just execute the following in a terminal: [1]

<pre><code>pip install marrow.schema</code></pre>

If you add @marrow.schema@ to the @install_requires@ argument of the call to @setup()@ in your application's @setup.py@ file, @marrow.schema@ will be automatically installed and made available when your own application is installed.  We recommend using "less than" version numbers to ensure there are no unintentional side-effects when updating.  Use @"marrow.schema<1.1"@ to get all bugfixes for the current release, and @"marrow.schema<2.0"@ to get bugfixes and feature updates, but ensure that large breaking changes are not installed.


h3(#install-dev). %2.1.% Development Version

Development takes place on "GitHub":github in the "marrow.schema":github-project project.  Issue tracking, documentation, and downloads are provided there.

Installing the current development version requires "Git":git, a distributed source code management system.  If you have Git, you can run the following to download and _link_ the development version into your Python runtime:

<pre><code>git clone https://github.com/marrow/marrow.schema.git
(cd marrow.schema; python setup.py develop)</code></pre>

You can upgrade to the latest version at any time:

<pre><code>(cd marrow.schema; git pull; python setup.py develop)</code></pre>

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes, and submit a pull request.  This process is beyond the scope of this documentation; for more information, see "GitHub's documentation":github-help.


[github]https://github.com/
[git]http://git-scm.com/
[github-help]http://help.github.com/



h2(#basic). %3.% Basic Usage



h3(#declaring). %3.1.% Declaring an Interface



h3(#api). %4.% Schema

The following schema classes are available.




h2(#license). %4.% License

Marrow Schema has been released under the MIT Open Source license.


h3(#license-mit). %8.1.% The MIT License

Copyright (C) 2013 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



fn1. If "Pip":http://www.pip-installer.org/ is not available for you, you can use @easy_install@ instead. We have much love for Pip and "Distribute":http://packages.python.org/distribute/, though.
