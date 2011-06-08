//	HYPE.documents["Cinema"]

(function HYPE_DocumentLoader() {
	var resourcesFolderName = "Cinema_Resources";
	var documentName = "Cinema";
	var documentLoaderFilename = "cinema_hype_generated_script.js";

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

var scenes = [{"timelines":{"kTimelineDefaultIdentifier":{"framesPerSecond":30,"animations":[{"startValue":"0.000000","isRelative":true,"endValue":"1.000000","identifier":"Opacity","duration":3,"timingFunction":"easeinout","type":0,"oid":"AEEE0641-FC76-4325-9E0D-6B7D0A4675CB-1109-0000037328005CA8","startTime":0},{"startValue":"302px","isRelative":true,"endValue":"60px","identifier":"Top","duration":3,"timingFunction":"easeinout","type":0,"oid":"AEEE0641-FC76-4325-9E0D-6B7D0A4675CB-1109-0000037328005CA8","startTime":0},{"startValue":"72px","isRelative":true,"endValue":"72px","identifier":"Left","duration":3,"timingFunction":"easeinout","type":0,"oid":"AEEE0641-FC76-4325-9E0D-6B7D0A4675CB-1109-0000037328005CA8","startTime":0}],"identifier":"kTimelineDefaultIdentifier","name":"Main Timeline","duration":3}},"id":"DD688399-B907-4D33-9B57-03B171016F88-1109-00000194A4978856","sceneIndex":0,"perspective":"600px","oid":"DD688399-B907-4D33-9B57-03B171016F88-1109-00000194A4978856","initialValues":{"B100FF72-13D4-488D-B28F-A70B28863C76-1109-0000032A0DF5E9B6":{"PaddingTop":"8px","FontFamily":"Arial,Helvetica,Sans-Serif","Position":"absolute","TagName":"div","PaddingRight":"8px","Display":"inline","Left":"16px","Overflow":"visible","ZIndex":"1","FontSize":"24px","TextColor":"#CCCCCC","WordWrap":"break-word","WhiteSpaceCollapsing":"preserve","PaddingBottom":"8px","PaddingLeft":"8px","Top":"16px","InnerHTML":"About Us"},"AEEE0641-FC76-4325-9E0D-6B7D0A4675CB-1109-0000037328005CA8":{"PaddingTop":"8px","Position":"absolute","InnerHTML":"<div>Faversham's Royal Cinema in the Market Place was reopened in 1994 by Peter Baldock and Michael Harlow. It was an immediate success and has gone from strength to strength. Over the years a huge amount of money - including £9,000 collected by the Royal Action Group (RAG) - has been invested in the building and its equipment.</div><div><br></div><div>The RAG funded a hundred new seats and repairs to the roof and guttering. The proprietors have upgraded the sound system to full Dolby Stereo Surround, having bought a new projector in 2001. Although we try to present something for everyone, we quickly discovered that the people of Faversham and beyond want good quality, serious films, hence our excellent relationship with the Faversham Film Society over many years.</div><div><br></div><div>Good family films are also in demand and most of the big budget block-busters are popular here. We have requests for classic films and repeats of not-so-new films. These presentations are usually well attended. Our uniformed staff are here to give friendly advice and help to customers, many of whom support the cinema on an incredibly regular basis - in fact we get worried when regulars don't appear on their usual night!</div><div><br></div><div>Known affectionately as 'a lovely little cinema', the Royal is actually quite large, built as an Odeon in 1936. It is one of only about 100 surviving original big-screen cinemas in the UK. The auditorium has not been reduced in size, although some of the seats, which originally numbered over 700, have been removed.</div><div>Parking is easy in the Bank Street car park, within 400 yards of the cinema. It is free in the evenings, of course.</div><div><br></div><div>The listed building's facade disguises its typical brick, concrete and steel construction. It is one of only two surviving mock-Tudor cinemas in the UK. The accomplished designer was the great cinema Andrew Mather, and his aim was to ensure that the building harmonised with its predominantly medieval surroundings - the town has nearly 500 other listed buildings, many of 13th-16th century date.</div><div><br></div><div>Together with the people, we have made the Royal a cinema of which the town is proud</div>","TagName":"div","PaddingRight":"8px","Display":"inline","Left":"72px","Height":"547px","Overflow":"visible","Width":"679px","ZIndex":"2","FontSize":"14px","TextColor":"#CCCCCC","WordWrap":"break-word","WhiteSpaceCollapsing":"preserve","PaddingBottom":"8px","PaddingLeft":"8px","Top":"302px","Opacity":"0.000000"}},"name":"History","backgroundColor":"#000000"}];

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
	hypeDoc.mainContentContainerID = "cinema_hype_container";
	hypeDoc.resourcesFolderName = resourcesFolderName;
	hypeDoc.showHypeBuiltWatermark = 0;
	hypeDoc.showLoadingPage = false;
	hypeDoc.drawSceneBackgrounds = true;
	hypeDoc.documentName = documentName;

	HYPE.documents[documentName] = hypeDoc.API;

	hypeDoc.documentLoad(this.body);
}());

