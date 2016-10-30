from clean_html import clean_html

doc_text1 = ["""<p>What am I doing wrong?</p>

<pre class=""lang-ts prettyprint-override""><code>import {bootstrap, Component} from 'angular2/angular2'

@Component({
  selector: 'conf-talks',
  template: `&lt;div *ngFor=""let talk in talks""&gt;
     {{talk.title}} by {{talk.speaker}}
     &lt;p&gt;{{talk.description}}
   &lt;/div&gt;`
})
class ConfTalks {
  talks = [ {title: 't1', speaker: 'Brian', description: 'talk 1'},
            {title: 't2', speaker: 'Julie', description: 'talk 2'}];
}
@Component({
  selector: 'my-app',
  directives: [ConfTalks],
  template: '&lt;conf-talks&gt;&lt;/conf-talks&gt;'
})
class App {}
bootstrap(App, [])
</code></pre>

<p>The error is</p>

<pre><code>EXCEPTION: Template parse errors:
Can't bind to 'ngForIn' since it isn't a known native property
(""&lt;div [ERROR -&gt;]*ngFor=""let talk in talks""&gt;
</code></pre>
""", """<p>My main issue was trying to loop for a certain number of times let's say n, but the <code>ngFor</code> only accepts arrays, like: ""<code>#item of [1, 2, ..., n]</code>"", so what is the proper way to loop using only the item count (without creating a useless array that has only numbers one to n)?</p>

<p>so I started reading more into the syntax and then i noticed that there are:</p>

<ul>
<li><code>*ngFor=""#item of items;</code></li>
<li><code>*ngFor=""#item in items;</code></li>
</ul>

<p>so what is the difference between ""in"" and ""of"" and what are there use cases? and does it have anything to do with my original case?</p>

<p>Thanks in advance.</p>
"""]

doc_text2 = ["""<p>When rendering a <a href=""http://dygraphs.com/options.html#stepPlot"" rel=""nofollow"">stepPlot</a> based dygraphs chart from multiple series containing gaps (encoded in the native data format as <code>NaN</code> per <a href=""http://dygraphs.com/options.html#connectSeparatedPoints"" rel=""nofollow"">documentation</a> and <a href=""http://dygraphs.com/tests/independent-series.html"" rel=""nofollow"">test examples</a>), I get occasional portions of the chart containing inconsistent dots/stroke patterns. Here is <a href=""http://jsfiddle.net/multidis/0xm8f383/4/"" rel=""nofollow"">JSFiddle</a>: scroll to the last chart. Please note that stroke itself is disabled (<code>strokeWidth: 0</code>), only fill should be present (intended behavior).</p>

<p>These inconsistencies appear even more visible with a denser chart:
<a href=""http://i.stack.imgur.com/Dy0jI.png"" rel=""nofollow""><img src=""http://i.stack.imgur.com/Dy0jI.png"" alt=""Dygraphs inconsistent stroke fill pattern""></a></p>

<p>Note that they appear not only at the boundary of different color steps but also at NaN/value step boundaries.</p>

<p>Is there some problematic combination of options that I am asking the chart to apply? Is it a dygraphs bug? Should data encoding be different? Thanks.</p>

""", """

<p>A div's width is not expanding with the width of its parent container or its content. There are no floats involved. The parent div has <code>overflow:scroll</code> and <code>white-space:pre</code> set; all else is normal. Identical behavior observed in Firefox, IE/Edge, Opera, and Chrome.</p>

<p><div class=""snippet"" data-lang=""js"" data-hide=""false"">
<div class=""snippet-code"">
<pre class=""snippet-code-css lang-css prettyprint-override""><code>div.wrapper {
  padding: 1em;
  width: 20em;
  background-color: rgb(240, 240, 240);
  overflow: scroll;
  white-space: pre;
  font-family: monospace;
}
div.line {
  background-color: rgb(200, 200, 200);
}
div.line span.blue {
  color: blue;
}
div.line span.green {
  color: green;
}</code></pre>
<pre class=""snippet-code-html lang-html prettyprint-override""><code>&lt;div class='wrapper'&gt;
  &lt;div class='line'&gt;This text is too &lt;span class=""blue""&gt;long&lt;/span&gt; for the wrapper div to &lt;span class=""green""&gt;contain&lt;/span&gt;, so the scroll bar activates.&lt;/div&gt;
  &lt;div class='line'&gt;However, the line div's background color fails to &lt;span class=""blue""&gt;expand&lt;/span&gt; with the longer contents, instead ending at the wrapper div's width. Why?&lt;/div&gt;
&lt;/div&gt;</code></pre>
</div>
</div>
</p>

<p>The background color of <code>div.line</code> extends as far as <code>div.wrapper</code>'s width on the page. But, when the user scrolls right, the text appears as normal while the <code>div.line</code>'s background color ends.</p>

<p>What I need is for every <code>div.line</code> to be as wide as <code>div.wrapper</code>'s ""inner"" width (to fill the scrollable area).</p>

<p>Failed solutions:</p>

<ul>
<li><p>set <code>overflow:hidden</code> - this hides the overflowing content, instead of resizing the div</p></li>
<li><p>set <code>overflow:auto</code> - this makes no difference</p></li>
<li><p>add <code>&lt;div style=""clear:both""&gt; &lt;/div&gt;</code> - makes no difference (no floats involved!)</p></li>
<li><p>set <code>after:...clear:both</code> - makes no difference, as above</p></li>
<li><p>set height on parent / child elements - makes no difference</p></li>
<li><p>set <code>width:auto</code> - made no difference</p></li>
</ul>

<p>I've researched this until my brain hurts. I really hope I'm missing something obvious.</p>


"""]

doc_text1 = [clean_html(x) for x in doc_text1]
doc_text2 = [clean_html(x) for x in doc_text2]