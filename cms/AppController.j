/*
 * AppController.j
 * CinemaCms
 *
 * Created by Ronald Hatcher on March 15, 2011.
 * Copyright 2011, Signature Interactive Solutions Limited All rights reserved.
 */

@import <Foundation/CPObject.j>
@import <AppKit/CPProgressIndicator.j>
@import "ICFilm.j"
@import "ICFilmSummary.j"

@implementation AppController : CPObject
{
    CPWindow    theWindow; //this "outlet" is connected automatically by the Cib
    @outlet CPButton theButton;
    @outlet CPSearchField theSearch;
    @outlet CPTableView theResults;
    @outlet CPTextField theFilmTitle;
    @outlet CPTextField thePlot;
    @outlet CPTextField theWriter;
    @outlet CPTextField theDirector;
<<<<<<< HEAD
    @outlet CPTextField theYear;
    @outlet CPTextField theTime;
=======
    @outlet CPTextField theTime;
    @outlet CPTextField theYear;
>>>>>>> feature-smart-search

    CPProgressIndicator waiter;
    CPArray films;
    ICFilm film;
    CPURLConnection _storeConnection; // Store a film command
    CPURLConnection _imdbConnection; // Search a fil command
}

- (void)applicationDidFinishLaunching:(CPNotification)aNotification
{
    // This is called when the application is done loading.
}

- (void)awakeFromCib
{
    // This is called when the cib is done loading.
    // You can implement this method on any object instantiated from a Cib.
    // It's a useful hook for setting up current UI values, and other things.

    // In this case, we want the window from Cib to become our full browser window
    [theWindow setFullBridge:YES];
    [theFilmTitle setStringValue:@""];
    [theWriter setStringValue:@""];
    [theDirector setStringValue:@""];
<<<<<<< HEAD
    [theYear setStringValue:@""];
    [theTime setStringValue:@""];
=======
    [theTime setStringValue:@""];
    [theYear setStringValue:@""];

>>>>>>> feature-smart-search
}

- (@action) click:(id)sender
{
/*    [theText setStringValue:@"hello world"];*/
}

- (@action) tableClick:(id)sender
{
    row = [sender selectedRow];
    var request = [CPURLRequest requestWithURL:"http://127.0.0.1:8000/imdb?action=store&id=" + encodeURIComponent([films[row] filmId])];

    [request setHTTPMethod: "GET"];
    _storeConnection = [CPURLConnection connectionWithRequest: request delegate: self];

}

- (id)displayFilm:(ICFilm)theFilm
{
    [theFilmTitle setStringValue:[theFilm title]];
    [thePlot setStringValue:[theFilm plotOutline]];
    [theWriter setStringValue:[theFilm writer]];
    [theDirector setStringValue:[theFilm director]];
<<<<<<< HEAD
    [theYear setStringValue:[theFilm year]];
    [theTime setStringValue:[theFilm runtimes]];
=======
    [theTime setStringValue:[theFilm runtimes]];
    [theYear setStringValue:[theFilm year]];
>>>>>>> feature-smart-search
}

- (@action) search:(id)Sender
{
    var userInput = [theSearch stringValue];

    if (userInput!=="") {
        var request = [CPURLRequest requestWithURL:"http://127.0.0.1:8000/imdb?action=search&title=" + encodeURIComponent(userInput)];

        [request setHTTPMethod: "GET"];
        _imdbConnection = [CPURLConnection connectionWithRequest: request delegate: self];
    }
}

// Datasource Methods

- (int)numberOfRowsInTableView:(CPTableView)tableView
{
    return [films count];
}

- (id)tableView:(CPTableView)tableView objectValueForTableColumn:(CPTableColumn)tableColumn row:(int)row
{
    if ([tableColumn identifier]===@"filmId")
        return [films[row] filmId];
    else
        return [films[row] title];
}

- (void)connection:(CPURLConnection)aConnection didReceiveData:(CPString)data
{
    //get a javascript object from the json response

    var result = JSON.parse(data);

    if (aConnection == _storeConnection) {
        film = [ICFilm initWithFilm:result];
        [self displayFilm:film];
    }

    if (aConnection == _imdbConnection) {
        films = [ICFilmSummary initWithJSONObjects:result];
        [theResults reloadData];
    }

    //clear out this connection's reference
    [self clearConnection:aConnection];
}

- (void)connection:(CPURLConnection)aConnection didFailWithError:(CPError)anError
{
    if (aConnection == _imdbConnection)
        alert("There was an error retrieving film information. Please try again in a moment.");

    [self clearConnection:aConnection];
}

- (void)clearConnection:(CPURLConnection)aConnection
{
    //we no longer need to hold on to a reference to this connection
    if (aConnection == _imdbConnection)
        _imdbConnection = nil;

    if (aConnection == _storeConnection)
        _storeConnection = nil;
}
@end
