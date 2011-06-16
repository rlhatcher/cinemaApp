//	HYPE.documents["Cinema-findus"]

(function HYPE_DocumentLoader() {
	var resourcesFolderName = "Cinema-findus_Resources";
	var documentName = "Cinema-findus";
	var documentLoaderFilename = "cinemafindus_hype_generated_script.js";

	// find the URL for this script's absolute path and set as the resourceFolderName
	try {
		var scripts = document.getElementsByTagName('script');
		for(var i = 0; i < scripts.length; i++) {
			var scriptSrc = scripts[i].src;
			if(scriptSrc != null && scriptSrc.indexOf(documentLoaderFilename) != -1) {
				resourcesFolderName = scriptSrc.substr(0, scriptSrc.lastIndexOf("/"));
				break;
			}
		}
	} catch(err) {	}

	// load HYPE.js if it hasn't been loaded yet
	if(typeof HYPE == "undefined") {
		if(typeof window.HYPE_DocumentsToLoad == "undefined") {
			window.HYPE_DocumentsToLoad = new Array();
		}
		window.HYPE_DocumentsToLoad.push(HYPE_DocumentLoader);

		var headElement = document.getElementsByTagName('head')[0];
		var scriptElement = document.createElement('script');
		scriptElement.type= 'text/javascript';
		scriptElement.src = resourcesFolderName + '/' + 'HYPE.js';
		headElement.appendChild(scriptElement);
		return;
	}
	
	var attributeTransformerMapping = {"BorderColorRight":"ColorValueTransformer","BackgroundColor":"ColorValueTransformer","BorderWidthBottom":"PixelValueTransformer","WordSpacing":"PixelValueTransformer","BoxShadowXOffset":"PixelValueTransformer","Opacity":"FractionalValueTransformer","BorderWidthRight":"PixelValueTransformer","BorderWidthTop":"PixelValueTransformer","BoxShadowColor":"ColorValueTransformer","BorderColorBottom":"ColorValueTransformer","FontSize":"PixelValueTransformer","BorderRadiusTopRight":"PixelValueTransformer","TextColor":"ColorValueTransformer","Rotate":"DegreeValueTransformer","Height":"PixelValueTransformer","PaddingLeft":"PixelValueTransformer","BorderColorTop":"ColorValueTransformer","Top":"PixelValueTransformer","BackgroundGradientStartColor":"ColorValueTransformer","TextShadowXOffset":"PixelValueTransformer","PaddingTop":"PixelValueTransformer","BackgroundGradientAngle":"DegreeValueTransformer","PaddingBottom":"PixelValueTransformer","PaddingRight":"PixelValueTransformer","Width":"PixelValueTransformer","TextShadowColor":"ColorValueTransformer","BorderColorLeft":"ColorValueTransformer","ReflectionOffset":"PixelValueTransformer","Left":"PixelValueTransformer","BorderRadiusBottomRight":"PixelValueTransformer","LineHeight":"PixelValueTransformer","BoxShadowYOffset":"PixelValueTransformer","ReflectionDepth":"FractionalValueTransformer","BorderRadiusTopLeft":"PixelValueTransformer","BorderRadiusBottomLeft":"PixelValueTransformer","TextShadowBlurRadius":"PixelValueTransformer","TextShadowYOffset":"PixelValueTransformer","BorderWidthLeft":"PixelValueTransformer","BackgroundGradientEndColor":"ColorValueTransformer","BoxShadowBlurRadius":"PixelValueTransformer","LetterSpacing":"PixelValueTransformer"};

var scenes = [{"timelines":{"kTimelineDefaultIdentifier":{"framesPerSecond":30,"animations":[{"startValue":"0.000000","isRelative":true,"endValue":"1.000000","identifier":"Opacity","duration":1.033333,"timingFunction":"easeinout","type":0,"oid":"A70DD3DE-573B-4AE4-9C03-78AB3FAA5C7F-31167-00014A31FB468C52","startTime":0}],"identifier":"kTimelineDefaultIdentifier","name":"Main Timeline","duration":1.033333}},"id":"14AFF182-BBAD-42B9-97ED-4D019CC2614D-31167-00014941E497CEFB","sceneIndex":0,"perspective":"600px","oid":"14AFF182-BBAD-42B9-97ED-4D019CC2614D-31167-00014941E497CEFB","initialValues":{"A70DD3DE-573B-4AE4-9C03-78AB3FAA5C7F-31167-00014A31FB468C52":{"BorderWidthBottom":"1px","TagName":"div","BorderColorBottom":"#A0A0A0","Opacity":"0.000000","BorderStyleRight":"Solid","BorderStyleBottom":"Solid","Top":"16px","BorderWidthRight":"1px","BorderStyleLeft":"Solid","BorderColorTop":"#A0A0A0","BorderColorLeft":"#A0A0A0","Position":"absolute","Height":"366px","Left":"23px","BorderColorRight":"#A0A0A0","InnerHTML":"<iframe width=\"661\" height=\"368\" frameborder=\"0\" scrolling=\"no\" marginheight=\"0\" marginwidth=\"0\" src=\"http://maps.google.com/maps?f=q&amp;source=s_q&amp;hl=en&amp;geocode=&amp;q=The+Royal+Cinema,+Faversham,+United+Kingdom&amp;sll=37.0625,-95.677068&amp;sspn=36.178967,78.134766&amp;ie=UTF8&amp;hq=The+Royal+Cinema,&amp;hnear=Faversham,+United+Kingdom&amp;ll=51.315969,0.890944&amp;spn=0.004023,0.006437&amp;z=16&amp;iwloc=A&amp;output=embed\"></iframe><br><small><a href=\"http://maps.google.com/maps?f=q&amp;source=embed&amp;hl=en&amp;geocode=&amp;q=The+Royal+Cinema,+Faversham,+United+Kingdom&amp;sll=37.0625,-95.677068&amp;sspn=36.178967,78.134766&amp;ie=UTF8&amp;hq=The+Royal+Cinema,&amp;hnear=Faversham,+United+Kingdom&amp;ll=51.315969,0.890944&amp;spn=0.004023,0.006437&amp;z=16&amp;iwloc=A\" style=\"color:#0000FF;text-align:left\">View Larger Map</a></small>","BorderStyleTop":"Solid","ZIndex":"1","Width":"659px","BorderWidthTop":"1px","Overflow":"visible","BorderWidthLeft":"1px","BackgroundColor":"#def"}},"name":"Untitled Scene","backgroundColor":"#000000"}];

var javascriptMapping = {};


	
	var Custom = (function() {
	return {
	};
}());

	
	var hypeDoc = new HYPE();
	
	hypeDoc.attributeTransformerMapping = attributeTransformerMapping;
	hypeDoc.scenes = scenes;
	hypeDoc.javascriptMapping = javascriptMapping;
	hypeDoc.Custom = Custom;
	hypeDoc.currentSceneIndex = 0;
	hypeDoc.mainContentContainerID = "cinemafindus_hype_container";
	hypeDoc.resourcesFolderName = resourcesFolderName;
	hypeDoc.showHypeBuiltWatermark = 0;
	hypeDoc.showLoadingPage = false;
	hypeDoc.drawSceneBackgrounds = true;
	hypeDoc.documentName = documentName;

	HYPE.documents[documentName] = hypeDoc.API;

	hypeDoc.documentLoad(this.body);
}());

