describe("The enumeration object", function () {
  it("BackgroundType should exist", function () {
    expect(BackgroundType).toBeDefined();
  });

  it("GradientType should exist", function () {
    expect(GradientType).toBeDefined();
  });

  it("HorizontalAlign should exist", function () {
    expect(HorizontalAlign).toBeDefined();
  });

  it("VerticalAlign should exist", function () {
    expect(VerticalAlign).toBeDefined();
  });

  it("AudioState should exist", function () {
    expect(AudioState).toBeDefined();
  });

  it("TransitionState should exist", function(){
    expect(TransitionState).toBeDefined();
  });

  it("AnimationState should exist", function(){
    expect(AnimationState).toBeDefined();
  });
});

describe("The function", function () {
  it("$() should return the right element", function () {
    var div = document.createElement("div");
    div.setAttribute("id", "dollar-test");
    document.body.appendChild(div);
    expect($("#dollar-test")[0]).toBe(div);
  });

  it("_buildLinearGradient() should build the correct string", function () {
    var gradient = _buildLinearGradient("left top", "left bottom", "#000", "#fff");
    expect(gradient).toBe("-webkit-gradient(linear, left top, left bottom, from(#000), to(#fff)) fixed");
  });

  it("_buildRadialGradient() should build the correct string", function () {
    var gradient = _buildRadialGradient(10, "#000", "#fff");
    expect(gradient).toBe("-webkit-gradient(radial, 10 50%, 100, 10 50%, 10, from(#000), to(#fff)) fixed");
  });

  it("_getStyle should return the correct style on an element", function () {
    var div = document.createElement("div");
    div.style.setProperty("width", "100px");
    div.setAttribute("id", "style-test");
    document.body.appendChild(div);
    expect(_getStyle($("#style-test")[0], "width")).toBe("100px");
  });

  it("_nl2br should turn UNIX newlines into <br> tags", function () {
    var text = "Amazing grace, how sweet the sound\nThat saved a wretch like me";
    expect(_nl2br(text)).toEqual("Amazing grace, how sweet the sound<br>That saved a wretch like me");
  });

  it("_nl2br should turn Windows newlines into <br> tags", function () {
    var text = "Amazing grace, how sweet the sound\r\nThat saved a wretch like me";
    expect(_nl2br(text)).toEqual("Amazing grace, how sweet the sound<br>That saved a wretch like me");
  });

  it("_prepareText should turn verse text into a paragraph", function () {
    var text = "Amazing grace, how sweet the sound\nThat saved a wretch like me";
    expect(_prepareText(text)).toEqual("<p>Amazing grace, how sweet the sound<br>That saved a wretch like me</p>");
  });
});

describe("The Display object", function () {
  it("should start with a blank _slides object", function () {
    expect(Display._slides).toEqual({});
  });

  it("should have the correct Reveal config", function () {
    expect(Display._revealConfig).toEqual({
      margin: 0.0,
      minScale: 1.0,
      maxScale: 1.0,
      controls: false,
      progress: false,
      history: false,
      overview: false,
      center: false,
      help: false,
      transition: "none",
      backgroundTransition: "none",
      viewDistance: 9999,
      width: "100%",
      height: "100%"
    });
  });

  it("should have an init() method", function () {
    expect(Display.init).toBeDefined();
  });

  it("should initialise Reveal when init is called", function () {
    spyOn(Reveal, "initialize");
    Display.init();
    expect(Reveal.initialize).toHaveBeenCalled();
  });

  it("should have a reinit() method", function () {
    expect(Display.reinit).toBeDefined();
  });

  it("should re-initialise Reveal when reinit is called", function () {
    spyOn(Reveal, "reinitialize");
    Display.reinit();
    expect(Reveal.reinitialize).toHaveBeenCalled();
  });

  it("should have a setTransition() method", function () {
    expect(Display.setTransition).toBeDefined();
  });

  it("should have a correctly functioning setTransition() method", function () {
    spyOn(Reveal, "configure");
    Display.setTransition("fade");
    expect(Reveal.configure).toHaveBeenCalledWith({"transition": "fade"});
  });

  it("should have a correctly functioning clearSlides() method", function () {
    expect(Display.clearSlides).toBeDefined();

    document.body.innerHTML = "";
    var slidesDiv = document.createElement("div");
    slidesDiv.setAttribute("class", "slides");
    slidesDiv.innerHTML = "<section><p></p></section>";
    document.body.appendChild(slidesDiv);

    Display.clearSlides();
    expect($(".slides")[0].innerHTML).toEqual("");
    expect(Display._slides).toEqual({});
  });

  it("should have a correct goToSlide() method", function () {
    spyOn(Reveal, "slide");
    spyOn(Display, "_slides");
    Display._slides["v1"] = 0;

    Display.goToSlide("v1");
    expect(Reveal.slide).toHaveBeenCalledWith(0);
  });

  it("should have an alert() method", function () {
    expect(Display.alert).toBeDefined();
  });

});

describe("Display.alert", function () {
  var alertBackground, alertText, settings;

  beforeEach(function () {
    document.body.innerHTML = "";
    alertBackground = document.createElement("div");
    alertBackground.setAttribute("id", "alert-background");
    document.body.appendChild(alertBackground);
    alertText = document.createElement("p");
    alertText.setAttribute("id","alert");
    alertBackground.appendChild(alertText);
    settings = '{ \
      "location": 1, "font_face": "Segoe UI, Tahoma, Geneva, Verdana, sans-serif", \
      "font_size": 40, "font_color": "#ffffff", "background_color": "#660000", \
      "timeout": 5, "repeat": 1, "scroll": true \
    }';
  });

  it("should return null if called without any text", function () {
    expect(Display.alert("",settings)).toBeNull();
  });

  it("should set the correct alert text", function () { 
    spyOn(Display, "setAlertKeyframes");    
    Display.alert("OPEN-LP-3.0 Alert Test", settings);
    
    expect(alertText.innerHTML).toEqual("OPEN-LP-3.0 Alert Test");
  });

  it("should call the addAlertToQueue method if an alert is displaying", function () {
    spyOn(Display, "addAlertToQueue");
    spyOn(Display, "setAlertKeyframes");
    Display._alerts = [];
    Display._alertState = AlertState.Displaying;
    var text = "Testing alert queue";
    
    Display.alert(text, settings);
    
    expect(Display.addAlertToQueue).toHaveBeenCalledWith(text, settings);
  });

  it("should set the alert settings correctly", function() {
    spyOn(Display, "setAlertKeyframes");
    Display.alert("Testing settings", settings);
        
    expect(Display._alertSettings).toEqual(JSON.parse(settings));
  });
});

describe("Display.showAlertBackground", function () {

  var alertBackground, bg_color;
  beforeEach(function () {
    document.body.innerHTML = "";        
    bg_color = "rgb(102, 0, 0)";
    alertBackground = document.createElement("div");
    alertBackground.setAttribute("id", "alert-background");
    alertBackground.setAttribute("class", "bg-default");    
    document.body.appendChild(alertBackground);           
  });

  it("should set the correct transition state", function () {
    Display.showAlertBackground(bg_color);
    expect(Display._transitionState).toEqual(TransitionState.EntranceTransition);
  });

  it("should apply the styles correctly when showAlertBackground is called", function () {
    Display.showAlertBackground(bg_color);    
         
    expect(alertBackground.style.backgroundColor).toEqual(bg_color);      
    expect(alertBackground.className).toEqual("bg-default show");                     
  });  
});

describe("Display.hideAlertBackground", function () {
  var alertBackground;
  beforeEach( function() {
    document.body.innerHTML = "";
    alertBackground = document.createElement("div");
    alertBackground.setAttribute("id", "alert-background"); 
    alertBackground.setAttribute("class", "bg-default show");     
    document.body.appendChild(alertBackground);    
  });
  
  it("reset the background to default once an alert has been displayed", function() {    
    Display.hideAlertBackground();
    
    expect(Display._transitionState).toEqual(TransitionState.ExitTransition);
    expect(Display._alertState).toEqual(AlertState.NotDisplaying);          
    expect(alertBackground.className).toEqual("bg-default");    
  });
});

describe("Display.setAlertText", function() {
  var alertText;
  beforeEach( function() {
    document.body.innerHTML = "";
    alertText = document.createElement("p");
    alertText.setAttribute("id", "alert");      
    document.body.appendChild(alertText);    
  });
  it("should set the alert text correctly", function () {    
    Display.setAlertText("OpenLP Alert Text");

    expect(alertText.textContent).toEqual("OpenLP Alert Text");
  });
});

describe("Display.setAlertLocation", function() {
  beforeEach(function() {
    document.body.innerHTML = "";    
    alertBackground = document.createElement("p");
    alertBackground.setAttribute("id","alert-background");
    alertBackground.setAttribute("class","bg-default");
    document.body.appendChild(alertBackground);
  });
  it("should set the correct class when location is top of the page", function () {    
    Display.setAlertLocation(0);

    expect(alertBackground.className).toEqual("bg-default top");
  });

  it("should set the correct class when location is middle of the page", function () {    
    Display.setAlertLocation(1);
    
    expect(alertBackground.className).toEqual("bg-default middle");       
  });

  it("should set the correct class when location is bottom of the page", function () {
    Display.setAlertLocation(2);

    expect(alertBackground.className).toEqual("bg-default bottom");
  });
});

describe("Display.removeAlertLocation", function () {
  beforeEach(function() {
    document.body.innerHTML = "";    
    alertBackground = document.createElement("p");
    alertBackground.setAttribute("id", "alert-background");
    alertBackground.setAttribute("class", "bg-default");
    document.body.appendChild(alertBackground);
  });
  it("should remove the correct class when location is top of the page", function () {
    alertBackground.classList.add("top");
    Display.removeAlertLocation(0);

    expect(alertBackground.className).toEqual("bg-default");
  });

  it("should remove the correct class when location is middle of the page", function () {
    alertBackground.classList.add("middle");
    Display.removeAlertLocation(1);
    
    expect(alertBackground.className).toEqual("bg-default");       
  });

  it("should remove the correct class when location is bottom of the page", function () {
    alertBackground.classList.add("bottom");
    Display.removeAlertLocation(2);

    expect(alertBackground.className).toEqual("bg-default");
  });
});

describe("Display.showAlertText", function () {
  var alertText, settings;
  beforeEach(function () {
    document.body.innerHTML = "";    
    alertText = document.createElement("p");
    alertText.setAttribute("id","alert");
    document.body.appendChild(alertText);
    settings = {
      "location": 2, "font_face": "Tahoma", "font_size": 40, 
      "font_color": "rgb(255, 255, 255)", "background_color": "rgb(102, 0, 0)",
      "timeout": 0.01, "repeat": 1, "scroll": true
    };
    Display._transitionState = TransitionState.EntranceTransition;
  });

  it("should set the correct styles on the text", function() {    
    Display.showAlertText(settings);    

    expect(alertText.style.opacity).toEqual('1');
    expect(alertText.style.color).toEqual("rgb(255, 255, 255)");
    expect(alertText.style.fontFamily).toEqual("Tahoma");
    expect(alertText.style.fontSize).toEqual("40pt");    
  });

  it("should set the correct animation when text is set to scroll)", function () {              
    Display.showAlertText(settings);

    expect(alertText.style.animation).toEqual("alert-scrolling-text " + settings.timeout + "s linear 0s 1 normal");
    expect(Display._animationState).toEqual(AnimationState.ScrollingText);    
  });

  it("should set the correct styles when text is not scrolling", function (done) {
    settings.scroll = false;       
    Display._transitionState = TransitionState.EntranceTransition;   
    spyOn(Display, "hideAlertText");    
    Display.showAlertText(settings);

    expect(alertText.style.opacity).toEqual('1');
    expect(alertText.style.animation).toEqual("");
    expect(Display._animationState).toEqual(AnimationState.NonScrollingText);    
    setTimeout (function () {
      expect(alertText.className).toEqual("no-scroll");
      expect(Display._animationState).toEqual(AnimationState.NoAnimation);
      expect(Display.hideAlertText).toHaveBeenCalled();      
      done();
    }, settings.timeout * 1000);
  });
});

describe("Display.hideAlertText", function() {
  var alertBackground, alertText, keyframeStyle;
  beforeEach(function () {
    document.body.innerHTML = "";
    // keyframeStyle = document.createElement("style");
    // keyframeStyle.setAttribute("id", "keyframeStyles");    
    // document.head.appendChild(keyframeStyle);
    // alertBackground = document.createElement("div");
    // alertBackground.setAttribute("id", "alert-background");
    // document.body.appendChild(alertBackground);
    alertText = document.createElement("p");
    alertText.setAttribute("id", "alert");
    alertText.style.opacity = 1;
    alertText.style.animation = "alert-scrolling-text 5s linear 0s 1 bg-default";
    document.body.appendChild(alertText);    
    Display._animationState = AnimationState.ScrollingText;
  });

  it("should reset the text styles and animation state after the text has scrolled", function() {
    spyOn(Display, "resetAlertKeyframes");
    spyOn(Display, "hideAlertBackground");    
    Display.hideAlertText();

    expect(alertText.style.animation).toEqual("");
    expect(alertText.style.opacity).toEqual('0');
    expect(alertText.style.color).toEqual("rgb(255, 255, 255)");
    expect(alertText.style.fontSize).toEqual("40pt");    
    expect(Display._animationState).toEqual(AnimationState.NoAnimation);
  });

  it("should call the hideAlertBackground and resetAlertKeyframes methods", function() {
    spyOn(Display, "hideAlertBackground");
    spyOn(Display, "resetAlertKeyframes");    
    Display.hideAlertText();

    expect(Display.hideAlertBackground).toHaveBeenCalled();
    expect(Display.resetAlertKeyframes).toHaveBeenCalled();
  });  
});

describe("Display.addAlertToQueue", function () {  
  it("should add an alert to the queue if one is displaying already", function() {
    Display._alerts = [];
    Display._alertState = AlertState.Displaying;
    settings = '{ \
      "location": 1, "font_face": "Segoe UI, Tahoma, Geneva, Verdana, sans-serif", \
      "font_size": 40, "font_color": "#ffffff", "background_color": "#660000", \
      "timeout": 5, "repeat": 1, "scrolling_text": true \
    }';
    var alertObject = {text: "Testing alert queue", settings: settings};
    var queuedAlert = JSON.stringify(alertObject);    
    
    Display.addAlertToQueue("Testing alert queue", settings);

    expect(Display._alerts.length).toEqual(1);
    expect(Display._alerts[0]).toEqual(queuedAlert);
  });
});

describe("Display.showNextAlert", function () {
  Display.showNextAlert();

  it("should return null if there are no alerts in the queue", function () {
    Display._alerts = [];
    Display.showNextAlert();

    expect(Display.showNextAlert()).toBeNull();
  });

  it("should call the alert function correctly if there is an alert in the queue", function () {    
    var settings = {
      "location": 2, "font_face": "Tahoma", "font_size": 40, 
      "font_color": "rgb(255, 255, 255)", "background_color": "rgb(102, 0, 0)",
      "timeout": 5, "repeat": 1, "scrolling_text": true
    };
    var alertObject = {text: "Queued Alert", settings: settings};
    Display._alerts.push(JSON.stringify(alertObject));
    spyOn(Display, "alert");    
    Display.showNextAlert();
    
    expect(Display.alert).toHaveBeenCalled();
    expect(Display.alert).toHaveBeenCalledWith("Queued Alert",alertObject.settings);
  });
});

describe("Display.alertTransitionEndEvent", function() {
  it("should set the correct state and call showAlertText after the alert entrance transition", function() {    
    var fake_settings = {test: "fake_settings"};  
    Display._alertSettings = fake_settings;
    spyOn(Display, "showAlertText");    
    Display._transitionState = TransitionState.EntranceTransition;    
    Display.alertTransitionEndEvent();

    expect(Display._transitionState).toEqual(TransitionState.NoTransition);
    expect(Display.showAlertText).toHaveBeenCalledWith(fake_settings);
  });
  
  it("should set the correct state after the alert exit transition", function() {        
    spyOn(Display, "showNextAlert");    
    Display._transitionState = TransitionState.ExitTransition;    
    Display.alertTransitionEndEvent();
    
    expect(Display._transitionState).toEqual(TransitionState.NoTransition);    
  });
});

describe("Display.alertAnimationEndEvent", function () {
  it("should call the hideAlertText method", function() {
    spyOn(Display, "hideAlertText");

    Display.alertAnimationEndEvent();

    expect(Display.hideAlertText).toHaveBeenCalled();
  });
});

describe("Display.setAlertKeyframes", function () {
  var keyframeStyle;
  beforeEach( function () {
    document.head.innerHTML = "";
    keyframeStyle = document.createElement("style");
    keyframeStyle.setAttribute("id", "keyframeStyles");
    document.head.appendChild(keyframeStyle);    
  });

  it("should set the correct keyframes", function () {
    var scrollWidth = 3200;
    var scrollWidthPercentage = (Math.ceil((((scrollWidth / screen.width) * 100) + 1) / 10) * 10) + 110;
    var keyframeHtml = "@keyframes alert-scrolling-text {" +
      "from { transform: translateX(110%); } " +
      "to { transform: translateX(-" + scrollWidthPercentage +"%);}";        
        
    expect(Display.setAlertKeyframes(scrollWidth)).toEqual(keyframeHtml);
    expect(keyframeStyle.innerHTML).toEqual(keyframeHtml);
  });
});

describe("Display.resetAlertKeyframes", function () {
  var keyframeStyle;
  beforeEach( function () {
    document.head.innerHTML = "";  
    keyframeStyle = document.createElement("style");
    keyframeStyle.setAttribute("id", "keyframeStyles");
    document.head.appendChild(keyframeStyle);
    keyframeStyle.innerHTML = "@keyframes alert-scrolling-text {" + 
                                "from { margin-left: 110%; } to { margin-left: -220;}";    
  });

  it("shoud reset the key frames after scrolling the text", function () {        
    Display.resetAlertKeyframes();

    expect(keyframeStyle.innerHTML).toEqual("");
  });
});

describe("Display.clearAlertSettings", function () {  
  it("should clear the alert settings once an alert has been displayed", function () {
    var fake_settings = {test: "fake_settings"};  
    Display._alertSettings = fake_settings;
    Display.clearAlertSettings();

    expect(Display._alertSettings).toEqual({});
  });
});

describe("Display.addTextSlide", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slidesDiv = document.createElement("div");
    slidesDiv.setAttribute("class", "slides");
    document.body.appendChild(slidesDiv);
    Display._slides = {};
  });

  it("should add a new slide", function () {
    var verse = "v1", text = "Amazing grace,\nhow sweet the sound";
    spyOn(Display, "reinit");

    Display.addTextSlide(verse, text);

    expect(Display._slides[verse]).toEqual(0);
    expect($(".slides > section").length).toEqual(1);
    expect($(".slides > section")[0].innerHTML).toEqual(_prepareText(text));
    expect(Display.reinit).toHaveBeenCalled();
  });

  it("should add a new slide without calling reinit()", function () {
    var verse = "v1", text = "Amazing grace,\nhow sweet the sound";
    spyOn(Display, "reinit");

    Display.addTextSlide(verse, text, false);

    expect(Display._slides[verse]).toEqual(0);
    expect($(".slides > section").length).toEqual(1);
    expect($(".slides > section")[0].innerHTML).toEqual(_prepareText(text));
    expect(Display.reinit).not.toHaveBeenCalled();
  });

  it("should update an existing slide", function () {
    var verse = "v1", text = "Amazing grace, how sweet the sound\nThat saved a wretch like me";
    Display.addTextSlide(verse, "Amazing grace,\nhow sweet the sound", false);
    spyOn(Display, "reinit");

    Display.addTextSlide(verse, text, true);

    expect(Display._slides[verse]).toEqual(0);
    expect($(".slides > section").length).toEqual(1);
    expect($(".slides > section")[0].innerHTML).toEqual(_prepareText(text));
    expect(Display.reinit).toHaveBeenCalled();
  });
});

describe("Display.setTextSlides", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slidesDiv = document.createElement("div");
    slidesDiv.setAttribute("class", "slides");
    document.body.appendChild(slidesDiv);

    var background = document.createElement("div");
    background.setAttribute("id", "global-background");
    document.body.appendChild(background);

    var footer = document.createElement("div");
    footer.setAttribute("class", "footer");
    document.body.appendChild(footer);

    Display._slides = {};
  });

  it("should add a list of slides", function () {
    var slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see"
      },
      {
        "verse": "v2",
        "text": "'twas Grace that taught, my heart to fear\nAnd grace, my fears relieved.\n" +
                "How precious did that grace appear,\nthe hour I first believed."
      }
    ];
    spyOn(Display, "clearSlides");
    spyOn(Display, "reinit");
    spyOn(Reveal, "slide");

    Display.setTextSlides(slides);

    expect(Display.clearSlides).toHaveBeenCalledTimes(1);
    expect(Display._slides["v1"]).toEqual(0);
    expect(Display._slides["v2"]).toEqual(1);
    expect($(".slides > section").length).toEqual(2);
    expect(Display.reinit).toHaveBeenCalledTimes(1);
    expect(Reveal.slide).toHaveBeenCalledWith(0);
  });

  it("should correctly set outline width", function () {
    const slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see"
      }
    ];

    const theme = {
      'font_main_color': 'yellow',
      'font_main_outline': true,
      'font_main_outline_size': 42,
      'font_main_outline_color': 'red'
    };

    spyOn(Display, "reinit");
    spyOn(Reveal, "slide");    

    Display.setTextSlides(slides);
    Display.setTheme(theme);

    const slidesDiv = $(".slides")[0];

    expect(slidesDiv.style['-webkit-text-stroke']).toEqual('42pt red');
    expect(slidesDiv.style['padding-left']).toEqual('84pt');
    expect(slidesDiv.style['-webkit-text-fill-color']).toEqual('yellow');
  })
});

describe("Display.setImageSlides", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slidesDiv = document.createElement("div");
    slidesDiv.setAttribute("class", "slides");
    document.body.appendChild(slidesDiv);
    var backgroundDiv = document.createElement("div");
    backgroundDiv.setAttribute("id", "global-background");
    document.body.appendChild(backgroundDiv);
    Display._slides = {};
  });

  it("should add a list of images", function () {
    var slides = [{"path": "file:///openlp1.jpg"}, {"path": "file:///openlp2.jpg"}];
    spyOn(Display, "clearSlides");
    spyOn(Display, "reinit");

    Display.setImageSlides(slides);

    expect(Display.clearSlides).toHaveBeenCalledTimes(1);
    expect(Display._slides["0"]).toEqual(0);
    expect(Display._slides["1"]).toEqual(1);
    expect($(".slides > section").length).toEqual(2);
    expect($(".slides > section > img").length).toEqual(2);
    expect($(".slides > section > img")[0].getAttribute("src")).toEqual("file:///openlp1.jpg")
    expect($(".slides > section > img")[1].getAttribute("src")).toEqual("file:///openlp2.jpg")
    expect(Display.reinit).toHaveBeenCalledTimes(1);
  });
});

describe("Display.setVideo", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slidesDiv = document.createElement("div");
    slidesDiv.setAttribute("class", "slides");
    document.body.appendChild(slidesDiv);
    var backgroundDiv = document.createElement("div");
    backgroundDiv.setAttribute("id", "global-background");
    document.body.appendChild(backgroundDiv);
    Display._slides = {};
  });

  it("should add a video to the page", function () {
    var video = {"path": "file:///video.mp4"};
    spyOn(Display, "clearSlides");
    spyOn(Display, "reinit");

    Display.setVideo(video);

    expect(Display.clearSlides).toHaveBeenCalledTimes(1);
    expect($(".slides > section").length).toEqual(1);
    expect($(".slides > section > video").length).toEqual(1);
    expect($(".slides > section > video")[0].src).toEqual("file:///video.mp4")
    expect(Display.reinit).toHaveBeenCalledTimes(1);
  });
});

describe("Display.playVideo", function () {
  var playCalled = false,
      mockVideo = {
        play: function () {
          playCalled = true;
        }
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should play the video when called", function () {
    Display.playVideo();
    expect(playCalled).toEqual(true);
  });
});

describe("Display.pauseVideo", function () {
  var pauseCalled = false,
      mockVideo = {
        pause: function () {
          pauseCalled = true;
        }
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should pause the video when called", function () {
    Display.pauseVideo();
    expect(pauseCalled).toEqual(true);
  });
});

describe("Display.stopVideo", function () {
  var pauseCalled = false,
      mockVideo = {
        pause: function () {
          pauseCalled = true;
        },
        currentTime: 10.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should play the video when called", function () {
    Display.stopVideo();
    expect(pauseCalled).toEqual(true);
    expect(mockVideo.currentTime).toEqual(0.0);
  });
});

describe("Display.seekVideo", function () {
  var mockVideo = {
        currentTime: 1.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should seek to the specified position within the video when called", function () {
    Display.seekVideo(7.34);
    expect(mockVideo.currentTime).toEqual(7.34);
  });
});

describe("Display.setPlaybackRate", function () {
  var mockVideo = {
        playbackRate: 1.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should set the playback rate of the video when called", function () {
    // Let's sound like chipmunks!
    Display.setPlaybackRate(1.25);
    expect(mockVideo.playbackRate).toEqual(1.25);
  });
});

describe("Display.setVideoVolume", function () {
  var mockVideo = {
        volume: 1.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should set the correct volume of the video when called", function () {
    // Make it quiet
    Display.setVideoVolume(30);
    expect(mockVideo.volume).toEqual(0.3);
  });
});

describe("Display.toggleVideoMute", function () {
  var mockVideo = {
        muted: false
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should mute the video when called", function () {
    mockVideo.muted = false;
    Display.toggleVideoMute();
    expect(mockVideo.muted).toEqual(true);
  });

  it("should unmute the video when called", function () {
    mockVideo.muted = true;
    Display.toggleVideoMute();
    expect(mockVideo.muted).toEqual(false);
  });
});

describe("AudioPlayer", function () {
  var audioPlayer, audioElement;

  beforeEach(function () {
    audioElement = {
      _eventListeners: {},
      _playing: false,
      _paused: false,
      _stopped: false,
      src: "",
      addEventListener: function (eventType, listener) {
        this._eventListeners[eventType] = this._eventListeners[eventType] || [];
        this._eventListeners[eventType].push(listener);
      },
      play: function () {
        this._playing = true;
        this._paused = false;
        this._stopped = false;
      },
      pause: function () {
        this._playing = false;
        this._paused = true;
        this._stopped = false;
      }
    };
    spyOn(document, "createElement").and.returnValue(audioElement);
    audioPlayer = new AudioPlayer();
  });

  it("should create an object", function () {
    expect(audioPlayer).toBeDefined();
    expect(audioPlayer._audioElement).not.toBeNull();
    expect(audioPlayer._eventListeners).toEqual({});
    expect(audioPlayer._playlist).toEqual([]);
    expect(audioPlayer._currentTrack).toEqual(null);
    expect(audioPlayer._canRepeat).toEqual(false);
    expect(audioPlayer._state).toEqual(AudioState.Stopped);
  });

  it("should call the correct method when _callListener is called", function () {
    var testCalled = false;
    function test(event) {
      testCalled = true;
    }
    audioPlayer._eventListeners["test"] = [test];
    audioPlayer._callListener({"type": "test"});
    expect(testCalled).toEqual(true);
  });

  it("should log a warning when _callListener is called for an unknown event", function () {
    spyOn(console, "warn");
    audioPlayer._callListener({"type": "test"});
    expect(console.warn).toHaveBeenCalledWith("Received unknown event \"test\", doing nothing.");
  });

  it("should add all the correct event listeners", function () {
    expectedListeners = {
      "ended": [audioPlayer.onEnded, audioPlayer._callListener],
      "timeupdate": [audioPlayer._callListener],
      "volumechange": [audioPlayer._callListener],
      "durationchange": [audioPlayer._callListener],
      "loadeddata": [audioPlayer._callListener]
    };
    expect(audioElement._eventListeners).toEqual(expectedListeners);
  });

  it("should add the correct event listener when calling addEventListener", function () {
    function dummy () {};
    var expectedListeners = {
      "test": [dummy]
    };
    audioPlayer.addEventListener("test", dummy);
    expect(audioPlayer._eventListeners).toEqual(expectedListeners);
  });

  it("should set call nextTrack when the onEnded listener is called", function () {
    spyOn(audioPlayer, "nextTrack");
    audioPlayer.onEnded({});
    expect(audioPlayer.nextTrack).toHaveBeenCalled();
  });

  it("should set the _canRepeat property when calling setCanRepeat", function () {
    audioPlayer.setCanRepeat(true);
    expect(audioPlayer._canRepeat).toEqual(true);
  });

  it("should clear the playlist when clearTracks is called", function () {
    audioPlayer._playlist = ["one", "two", "three"];
    audioPlayer.clearTracks();
    expect(audioPlayer._playlist).toEqual([]);
  });

  it("should add a track to the playlist when addTrack is called", function () {
    audioPlayer._playlist = [];
    audioPlayer.addTrack("one");
    expect(audioPlayer._playlist).toEqual(["one"]);
  });

  it("should move to the first track when canRepeat is true and nextTrack is called", function () {
    spyOn(audioPlayer, "play");
    audioPlayer.addTrack("one");
    audioPlayer.addTrack("two");
    audioPlayer.setCanRepeat(true);
    audioPlayer._currentTrack = "two";

    audioPlayer.nextTrack();

    expect(audioPlayer.play).toHaveBeenCalledWith("one");
  });

  it("should move to the next track when nextTrack is called", function () {
    spyOn(audioPlayer, "play");
    audioPlayer.addTrack("one");
    audioPlayer.addTrack("two");
    audioPlayer._currentTrack = "one";

    audioPlayer.nextTrack();

    expect(audioPlayer.play).toHaveBeenCalledWith("two");
  });

  it("should stop when canRepeat is false and nextTrack is called on the last track in the list", function () {
    spyOn(audioPlayer, "play");
    spyOn(audioPlayer, "stop");
    audioPlayer.addTrack("one");
    audioPlayer.addTrack("two");
    audioPlayer.setCanRepeat(false);
    audioPlayer._currentTrack = "two";

    audioPlayer.nextTrack();

    expect(audioPlayer.play).not.toHaveBeenCalled();
    expect(audioPlayer.stop).toHaveBeenCalled();
  });

  it("should play the first track when nextTrack is called when no songs are playing", function () {
    spyOn(audioPlayer, "play");
    audioPlayer.addTrack("one");
    audioPlayer.nextTrack();
    expect(audioPlayer.play).toHaveBeenCalledWith("one");
  });

  it("should log a warning when nextTrack is called when no songs are in the playlist", function () {
    spyOn(console, "warn");
    audioPlayer.nextTrack();
    expect(console.warn).toHaveBeenCalledWith("No tracks in playlist, doing nothing.");
  });

  it("should play the track specified when play is called with a filename", function () {
    audioPlayer.addTrack("one");
    audioPlayer.play("one");

    expect(audioPlayer._currentTrack).toEqual("one");
    expect(audioElement._playing).toEqual(true);
    expect(audioElement.src).toEqual("one");
    expect(audioPlayer._state).toEqual(AudioState.Playing);
  });

  it("should continue playing when play is called without a filename and the player is paused", function () {
    audioPlayer._state = AudioState.Paused;
    audioPlayer.play();

    expect(audioElement._playing).toEqual(true);
    expect(audioPlayer._state).toEqual(AudioState.Playing);
  });

  it("should do nothing when play is called without a filename and the player is not paused", function () {
    spyOn(console, "warn");
    audioPlayer._state = AudioState.Playing;
    audioPlayer.play();

    expect(console.warn).toHaveBeenCalledWith("No track currently paused and no track specified, doing nothing.");
  });

  it("should pause the current track when pause is called", function () {
    audioPlayer.pause();
    expect(audioPlayer._state).toEqual(AudioState.Paused);
    expect(audioElement._paused).toEqual(true);
  });

  it("should stop the current track when stop is called", function () {
    audioPlayer.stop();
    expect(audioPlayer._state).toEqual(AudioState.Stopped);
    expect(audioElement._paused).toEqual(true);
    expect(audioElement.src).toEqual("");
  });
});
