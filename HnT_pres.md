# <span style="text-transform: lowercase;">ar<span style="text-transform: uppercase;">X</span>iv2git</span>
----------
### [Travis Hoppe](http://thoppe.github.io/)
[https://github.com/thoppe/arXiv2git](https://github.com/thoppe/arXiv2git)

====

### What is the
!(https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/ArXiv_web.svg/2000px-ArXiv_web.svg.png) <<transparent; height:200px>>

pre-print server for physicists, mathematicians, computer scientists
over _1 million_ papers, 100 million paper downloads / year
full of seminal papers and 100% free worldwide, rapid-publication
butt-ugly and little/no meta information and linking
  
====*

### What is [github](https://github.com)?
!(https://cdn.tutsplus.com/net/uploads/2013/08/github-collab-retina-preview.gif) <<height:200px>>
  
Open source storage for 35 million projects and millions of users.
_de-facto_ standard for publishing code.

====

## Problem?
+ paper is published to the arXiv
+ code is pushed to github
+ new researcher can't find code from paper?
+ ...
+ opposite of profit
  

!(figures/anger.gif) <<width:500px; transparent>>
 
=====

enter
# <span style="text-transform: lowercase;">ar<span style="text-transform: uppercase;">X</span>iv2git</span>
links arXiv papers to github repositories!
[https://github.com/thoppe/arXiv2git](https://github.com/thoppe/arXiv2git)
  
====+
It's a chrome extension!
[https://chrome.google.com/webstore/detail/arxiv2git/](https://chrome.google.com/webstore/detail/arxiv2git/gfhbipbocjiapodeflmklgnnnndplnpp)
!(figures/screen.png) 

=====

## How does it work?

Static scrape of github search API
Download/clone all results with `arXiv` in README
Parse out potential links and references
Build a static json for each arXiv paper

Build chrome extension locally (surprisingly easy!)
Pay $5 and register extension on chrome store
Have app pull saved json from github
Inject results into any arXiv page that matches

====
### Live demo goes [here](http://arxiv.org/abs/1512.03385) ...
!(figures/example_screen.png) Screenshot since live demos always fail

====
  

#  Thanks, you!
Say hello: [@metasemantic](https://twitter.com/metasemantic)