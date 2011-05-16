@import <AppKit/AppKit.j>
@import <Foundation/Foundation.j>

@import "Film.j"

@implementation FilmController : CPWindowController
{
    CPArray films @accessors;
}

-(id)init
{
    self = [super init];

    return self;
}

-(id)initWithFilms:(CPArray)theFilms
{
    self = [super init];

    if (self) {
        films = theFilms;
    };

    return self;
}

-(void)awakeFromCib
{
    CPLog.debug(@"%s %s self :  %@",[self class],_cmd,self);

    CPLog.debug(@"%s %s  [films count] :  %@",[self class],_cmd, [films count]);
}

@end