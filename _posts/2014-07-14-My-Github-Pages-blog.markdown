
---
layout: post
title: My Github Pages blog
category: start ups
tags: jekyll bootstrap github disqus
year: 2014
month: 7
day: 14
published: true
summary: A tutorial on how I built my blog
image: post_one.jpg
---
<emph>Good artists borrow, great artists steal!</emph>

<div class="row">	
	<div class="span9 columns">
	  <h2>Preface</h2>
	  <p>I basically stole this whole template from <a href=http://erjjones.github.io/" target="_blank">Eric Jones</a>. I followed his <a href="http://erjjones.github.io/blog/How-I-built-my-blog-in-one-day/" target="_blank">How-I-built-my-blog-in-one-day</a> post nearly exactly... well, except for where I stopped (No comments yet).

Mostly this has been a copy and paste effort. I will be adding notes on special circumstances later.

This is where I left off...

	  <h2>Disqus</h2>
	  <p>To me it made perfect sense to use <a href="http://disqus.com/" target="_blank" title="Go to Disqus">Disqus</a> as a comments provider.  As far as I can tell lots of sites are using this provider so we'll see how it goes.  When you setup an account Disqus will have you setup a <i>shortname</i> that you will use in your Disqus widget code.  The <i>Admin</i> tools in Disqus will allow you to delete comments and set a list of blackout words.</p>	  
	  <h2><small>Total Comments</small></h2>	
	  <p>To get the <a href="http://ehrlinger.github.io{{ page.url }}#disqus_thread" data-disqus-identifier="{{ page.url }}"></a> you can put the following code anywhere on your page or any other page as long as you use the url you would like and have the Disqus Widget code on your page, it just works.</p>
	  <p><pre><code>&lt;a href="http://ehrlinger.github.io&#123;&#123; page.url &#125;&#125;#disqus_thread" data-disqus-identifier="&#123;&#123; page.url &#125;&#125;"&gt;&lt;/a&gt;</code></pre></p>	  
	  <h2><small>Disqus Widget Code</small></h3>	
	  <script src="https://gist.github.com/1998023.js"> </script>
	  <hr>
	  <h2>Jekyll Continued</h2>
	  <h2><small>Pages and Properties</small></h2>	
	  <p>Using Jekyll you save your blog posts as <code>.markdown</code> files which contain a header section like the code sample below and html, css, javascript, etc.</p>
	  <script src="https://gist.github.com/1998470.js"> </script>
	  <p>To create the header of every blog post I simply <i>include</i> a template header that has the following properties set.</p>	
	  <p><pre><code>&lt;h4&gt;&lt;strong&gt;&#123;&#123; page.date | date: "%B %e, %Y" &#125;&#125; &lt;small&gt;. &#123;&#123; page.category &#125;&#125; .&lt;/small&gt; &#123;&#123; page.title &#125;&#125;&lt;/strong&gt;&lt;/h4&gt;</code></pre></p>	  
	  <h4><strong>{{ page.date | date: "%B %e, %Y" }} <small>. {{ page.category }} .</small> {{ page.title }}</strong></h4>
	  <br/>
	  <h2><small>Listing all your posts</small></h2>	
	  <p>On the home page I list all of the blog posts.  The code below will allow you to list all of your posts in the <code>_posts</code> folder.  By naming the .markdown files with the date in the file name like <code>2012-03-08-How-I-built-my-blog.markdown</code></p>	
	  <script src="https://gist.github.com/1998382.js"> </script>	  
	  <br/>
	  <h2><small>Paging</small></h3>	
	  <p>Ideally this blog would take on the characteristics of a blogazine like feel.  One way I try to achieve that is through pagination.  On the top of each of the blogs I use <i class="icon-chevron-left"></i><i class="icon-chevron-right"></i> and <a href="#" title="Previous Post: {{page.previous.title}}">&laquo; Previous Blog Post</a> | <a href="#" title="Next Post: {{page.next.title}}">Next Blog Post &raquo; </a> at the bottom.</p>	  
	  <script src="https://gist.github.com/1998418.js"> </script>
	  <hr>
	  <h2>Instapaper</h2>
	  <p>Adding an <a href="http://www.instapaper.com" target="_blank" title="Go to Instapaper">Instapaper</a> link is just another piece of functionality to enhance integration with other web tools.  All you need to do is build the link below and add your <i>url</i> and <i>title</i>.</p>	
	  <p><pre><code>http://www.instapaper.com/hello2?url=http://ehrlinger.github.io&#123;&#123; page.url &#125;&#125;&title=&#123;&#123; page.title &#125;&#125;</code></pre></p>
	  <p><a href="http://www.instapaper.com/hello2?url=http://ehrlinger.github.io{{ page.url }}&title={{ page.title }}" title="Save {{ page.title }} to Instapaper" target="_blank">Read later</a></p>
	  <hr>	  
	  <h2>Y Combinator Submit Icon</h2>
	  <p><a href="http://news.ycombinator.com/" target="_blank" title="Go to news.ycombinator.com">Y Combinator</a> is my all time favorite news feed and adding a Y Combinator submit option just seemed right.  All you need to do is build the link below and add your <i>url</i> and <i>title</i>.</p>	
	  <p><pre><code>http://news.ycombinator.com/submitlink?u=http://ehrlinger.github.io&#123;&#123; page.url &#125;&#125;&t=&#123;&#123; page.title &#125;&#125;</code></pre></p>
	  <p><a href="http://news.ycombinator.com/submitlink?u=http://ehrlinger.github.io{{ page.url }}&t={{ page.title }}" target="_blank"><img src="/img/yc500.gif" title="Submit {{ page.title }} to Hacker News" /></a></p>
	  <hr>		  	  	  
	  <h2>In Conclusion</h2>
	  <p>I hope this sparks you to try out GitHub, Jekyll, Twitter Bootstrap and other open source web resources.  I have just begun to scratch the surface here and this blog doesn't attempt to cover all of details but I would like to hear what other cool integrations people are doing on their blogs.</p>	  
	  <hr>
	</div>
</div> 

<div class="row">	
	<div class="span9 column">
			<p class="pull-right">{% if page.previous.url %} <a href="{{page.previous.url}}" title="Previous Post: {{page.previous.title}}"><i class="icon-chevron-left"></i></a> 	{% endif %}   {% if page.next.url %} 	<a href="{{page.next.url}}" title="Next Post: {{page.next.title}}"><i class="icon-chevron-right"></i></a> 	{% endif %} </p>  
	</div>
</div>

<div class="row">	
    <div class="span9 columns">    
		<h2>Comments Section</h2>
	    <p>Feel free to comment on the post but keep it clean and on topic.</p>	
		<div id="disqus_thread"></div>
		<script type="text/javascript">
			/* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
			var disqus_shortname = 'ericjones'; // required: replace example with your forum shortname
			var disqus_identifier = '/blog/How-I-built-my-blog-in-one-day';
			var disqus_url = '/blog/How-I-built-my-blog-in-one-day';
			
			/* * * DON'T EDIT BELOW THIS LINE * * */
			(function() {
				var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
				dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
				(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
			})();
		</script>
		<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
		<a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
	</div>
</div>

<!-- Twitter -->
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>

<!-- Google + -->
<script type="text/javascript">
  (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();
</script>