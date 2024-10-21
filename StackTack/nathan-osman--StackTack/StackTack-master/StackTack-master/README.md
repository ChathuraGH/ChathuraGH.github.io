<h2>StackTack</h2>
<p>StackTack is a tool that will fetch information about any question in the Stack Exchange network of sites and format it in a nicely-styled and functional widget.</p>

<h3>What Has Been Changed</h3>
<p>This fork contains a number of changes from the <a href="https://bitbucket.org/zamtools/stacktack">original code</a>. The details of these changes are below:</p>
<ul>
  <li>The icons and images in the sprite were removed.</li>
  <li>A build system for minifying the CSS and JS was added.</li>
  <li><code>.stacktack()</code> now operates on the current set of matched elements instead of searching for elements based on ID.</li>
  <li>Options can be specified globally yet overridden on a per-invocation and per-element basis (including <code>site</code>).</li>
  <li>API requests to the same site are grouped to cut down on requests.</li>
</ul>

<h3>Dependencies</h3>
<ul>
  <li>jQuery (only if built with <code>--disable-jquery-check</code>)</li>
</ul>

<h3>Build Dependencies</h3>
<ul>
  <li>Python 2.5+ (required by the build system, <a href="https://github.com/nathan-osman/Juice-Builder">Juice Builder</a>)</li>
</ul>

<h3>Build Instructions</h3>
<ol>
  <li>Determine whether you want the CSS styles to be included in the minified JS file or whether you want to create an external minified CSS file.</li>
  <li>
    Run the following command:
    <pre><code>python build.py</code></pre>
    <b>Note:</b> add the <code>--enable-embed-css</code> option to the command above if you want to embed the CSS.
  </li>
  <li>You should now have a 'stacktack.min.js' file and (depending on the options you specified) a 'style.min.css' file in the 'out' folder.</li>
</ol>

<h3>Using StackTack</h3>
<p>Adding StackTack to a page is relatively simple and consists of the following steps:</p>
<ol>
  <li>
    If you <b>did not</b> build StackTack with the <code>--enable-embed-css</code> option, add the following line to the <code>&lt;head&gt;</code> section of your page:
    <pre><code>&lt;link rel="stylesheet" href="style.min.css" /&gt;</code></pre>
  </li>
  <li>
    If you built StackTack with the <code>--disable-jquery-check</code> option, you will need to manually load jQuery by adding the following to the end of the <code>&lt;body&gt;</code> section of your page:
    <pre><code>&lt;script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"&gt;&lt;/script&gt;</code></pre>
  </li>
  <li>
    Add StackTack to the <code>&lt;body&gt;</code> section of your page:
    <pre><code>&lt;script type="text/javascript" src="stacktack.min.js"&gt;&lt;/script&gt;</code></pre>
  </li>
  <li>
    If you <b>did not</b> build StackTack with the <code>--disable-jquery-check</code> option, add the following lines directly below the one above:
    <pre><code>&lt;script type="text/javascript"&gt;
$(document).ready(function() {
    $('.stacktack').stacktack();
});
&lt;/script&gt;</code></pre>
    This little snippet initializes all of the elements on the page with the 'stacktack' class.
  </li>
  <li>
    To insert a StackTack widget on the page, use the following template:
    <pre><code>&lt;div class="stacktack" data-site="stackoverflow" data-id="1732348" &gt;&lt;/div&gt;</code></pre>
    The <code>&lt;div&gt;</code> contains a number of <code>data-*</code> attributes that specify the options for that particular instance. These options include:
    <ul>
      <li><b>answers:</b> specifies the answers that will be displayed - this can be 'all', 'none', 'accepted', or a comma-separated list of answer IDs</li>
      <li><b>id:</b> the ID of the question <i>[required]</i></li>
      <li><b>question:</b> whether or not to display the question</li>
      <li><b>secure:</b> whether to use HTTPS when retrieving data from the API</li>
      <li><b>site:</b> the site to retrieve the question from</li>
      <li><b>tags:</b> whether or not to display the question's tags</li>
      <li><b>votes:</b> whether or not to display vote score on answers</i>
      <li><b>width:</b> the width (in pixels) of the widget</li>
    </ul>
    These options (except 'id') can also be specified in a map in the <code>.stacktack()</code> method in the previous step.
  </li>
</ol>