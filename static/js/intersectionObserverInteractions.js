
/* Small js function to detect users scroll bar position and activate the sticky navigator
Should only work on screens ~768px - 1980px , this behavior should not occur on mobile.
In that case the navigator is absolutely positoned as the first element of the class "narrow" */

/* 
	CSS/BOOTSTRAP BREAKPOINTS:(Where the layout is adjusted when screen width reaches below a certain threshold)
	==> width < 1260px: 
		Navigator and position styling needs to be adjusted, honestly all elements in this window (768px - 1260px) look misaligned,
		going to need to fix that.
		Generally this styling works but the boot strap needs to be edited later
   			position: absolute;
    		left: -23.5%;
    		margin: 0 auto;
    		top: 1.1%;
	==> width < 768px: Navigator should be absolutely positioned at top of "narrow" class div. 
	Do this through CSS Stlying/ media queries 
*/


var root_in = null;//Means monitor viewport
var root_margin_in = "0px"
var threshold_in = 0.0 //means that when 0% of the target is visible within the element specified by the root option, the callback is invoked.
var width_break_point = 768; // Navigator is not sticky if width is less than this value

options = {
	root:root_in, 
	rootMargin:root_margin_in,
	threshold: threshold_in 
}

//Listen to document onces it is done loading and get a reference to the DOM element with id #navigator
window.addEventListener("load",function(event){
	image_elem = document.querySelector("#fore");
	//nav_elem = document.querySelector("#navigator");
	createObserver(options,image_elem,stickyNavigation);
}, false);

/* 
	Creates observer object to watch interaction between 2 elements via Intersection Observer API 
	-options: array of key value pairs to pass in to create observer object
	-elem: 	The specifed elem (DOM object) to be observed by the observer object.
*/
function createObserver(options , elem, observer_call_back ){
	var observer = new IntersectionObserver(observer_call_back,options);
	console.log("Successfully created observer for navigator!");
	observer.observe(elem);
}	

/* 
	Callback function to react to when elem is 100% in viewport (the navigator). Adds CSS styling to make
	it fixed. Only works if screen width is between 768px and 1980px 
	-entries: array of IntersectionObserverEntry objects
	-observer: The observer that the object the callback was executed on 
*/
function stickyNavigation(entries, observer){
	 //Check the width, should not activate if width < 768px
	 width = window.innerWidth;
	 nav_elem = document.querySelector("#navigator");
	 if(width > 768){
	 	entries.forEach(function(entry){
	 		if(entry.intersectionRatio > 0 && entry.intersectionRatio <= .2){
	 			console.log("Intersection ratio of #fore is " + entry.intersectionRatio);
	 			//entry.target.setAttribute("style","position:fixed; left:-3%; max-width:15%; top:22%;");
	 			nav_elem.setAttribute("style","position:fixed; left:-1%; max-width:15%; top:22%;");
	 			console.log(entry);
	 			console.log("Successfully changed navigtors CSS properties!");
	 			//This needs to be changed
	 		}else if(entry.intersectionRatio > .3){
	 			console.log("Intersection ratio of #fore is (in applying default nav style) " + entry.intersectionRatio);
	 			//Apply default styling, is this redunant, need to look at the implications of this later 
	 			//entry.target.setAttribute("style","position:absolute; left:-23.5%; margin: 0 auto; top:1.1%;");	
	 			nav_elem.setAttribute("style","position:absolute; left:-23.5%; margin: 0 auto; top:1.1%;");
	 		}
	 	});
	 }
}

   	
    