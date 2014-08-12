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
			var disqus_shortname = 'johnehrlinger'; // required: replace example with your forum shortname
			var disqus_identifier = '/blog/My-Github-Pages-blog';
			var disqus_url = '/blog/My-Github-Pages-blog';
			
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