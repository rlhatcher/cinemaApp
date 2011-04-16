@import <Foundation/CPObject.j>

@implementation ICFilmSummary : CPObject
{
    CPString filmId         @accessors;
    CPString title          @accessors;
}

- (id)initWithJSONObject:(JSObject)anObject
{
    self = [super init] ;

    if (self) {
        filmId    = anObject.id;
        title     = anObject.title;
    }

    return self;
}

+ (CPArray)initWithJSONObjects:(CPArray)someJSONObjects
{
    var films   = [[CPArray alloc] init];

    for (var i=0; i < someJSONObjects.length; i++) {
        var film = [[ICFilmSummary alloc] initWithJSONObject:someJSONObjects[i]] ;
        [films addObject:film] ;
    };

    return films ;
}

@end
