@import <Foundation/CPObject.j>

@implementation ICFilm : CPObject
{
    CPString _filmId        @accessors(property=filmId);
    CPString _title         @accessors(property=title);
    CPString _year          @accessors(property=year);
    CPString _plotOutline   @accessors(property=plotOutline);
    CPString _plot          @accessors(property=plot);
    CPString _director      @accessors(property=director);
    CPString _writer        @accessors(property=writer);
    CPString _cast          @accessors(property=cast);
    CPString _runtimes      @accessors(property=runtimes);
}

- (id)init
{
    self = [super init] ;

    return self;
}

+ (ICFilm)initWithFilm:(JSObject)anObject
{
    var film = [[ICFilm alloc] init];

    [film setFilmId:anObject.id];
    [film setTitle:anObject.title];
    [film setYear:anObject.year];
    [film setPlotOutline:anObject.plotOutline];
    [film setPlot:anObject.plot];
    [film setDirector:anObject.director];
    [film setWriter:anObject.writer];
    [film setCast:anObject.cast];
    [film setRuntimes:anObject.runtimes];

    return film;
}
@end
