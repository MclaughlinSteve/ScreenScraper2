#! /usr/bin/perl -w
#
# Scrape2.cgi - Displays the weekly Penny Arcade comic strip
#              
# Steve McLaughlin
# I did this in a way that didn't use the "next" buttons, but I used DateTime instead to
# generate the urls for each comic every week
#
# Note to Dr. Provine: If you need me to change this to navigate via the 'next' buttons, please
# let me know, and I will change it. It should be a quick/easy change if it's necessary.
#
# I tried to document this and make it as readable as possible, but this is perl. Good luck.


use strict;
use CGI;
use WWW::Mechanize;
use HTML::TokeParser;
use DateTime;

# find last Sunday
my $date = DateTime->now;
$date->subtract( hours=> 4); #This should make the date in my time zone (EST)
my $numComics = 1; #The number of comics published this week
while ( $date->day_of_week != 1 ) {
	$date->subtract( days => 1 );
	$numComics++;

}


#This is some sample input just to test if it pulled the whole week's comics (I wrote this on a monday
# so only one comic was published for the week at the time.) It worked for the previous week.
#
#$date->subtract(days=>0);
#$numComics = 1;


#This is used to make sure that a false link isn't attempted if accessed on a sunday.
# Otherwise, another little image will show up on the page on sundays.
#
# There is probably a more elegant way to go about this, but this works for now 

if($numComics >= 6)
	{$numComics=6;}


# format the date the way the URL needs to look:
my $target = sprintf("%d/%02d/%02d",
                     $date->year(), $date->month(), $date->day() );



# create CGI object and generate HTML:
my $cgi = new CGI;

print $cgi->header(-type=>'text/html'),
      $cgi->start_html(-title=>'Weekly Penny Arcade',
			-author=>'Steve McLaughlin',
			-style=>{'src'=>'/~mclaug67/style.css'});
print $cgi->h1('<a href = "http://www.penny-arcade.com/comic/">Penny Arcade (Weekly version)</a>');

# Loop runs for as many comics as previously calculated
for(my $i=1; $i <= $numComics; $i+=2)
{
	# Update the target url
	my $target = sprintf("%d/%02d/%02d",
                     $date->year(), $date->month(), $date->day() );
	my $agent = WWW::Mechanize->new();

	#debugging
	#print $cgi->p('<a href = "http://www.penny-arcade.com/comic/'.$target.'">'.Test.'</a>');
	#print $cgi->p($i);



	# Go to the url for the specific day's comic
	$agent->get("http://www.penny-arcade.com/comic/" . $target) ;
	my $stream = HTML::TokeParser->new(\$agent->{content});

	# find the div tag with the comic in it
	my $tag = $stream->get_tag("div");

	while ( $tag->[1]{class} and $tag->[1]{class} ne 'comicFrame' ) {
    		$tag = $stream->get_tag("div");
	}	

	# find the comic image itself
	my $toon = $stream->get_tag("img");

	# locate the source file for the comic
	my $source = $toon->[1]{'src'};

	# display the comic on the screen
	print $cgi->img({src=> $source}), "\n\n";
	$date->add( days => 2); # Penny arcade updates mon, wed, fri so there will always be a 2 day break

}


# ALL DONE!

print $cgi->hr();
print $cgi->p('
    <a href ="http://validator.w3.org/check/referer">
        <img style="border:0;width:88px:height:31px"
            src="http://www.w3.org/Icons/valid-xhtml11"
            alt="Valid XHTML 1.1!">
    </a>

    <a href="http://jigsaw.w3.org/css-validator/check/referer">
        <img style="border:0;width:88px;height:31px"
            src="http://jigsaw.w3.org/css-validator/images/vcss"
            alt="Valid CSS!" />
    </a>
');

print $cgi->end_html, "\n";

