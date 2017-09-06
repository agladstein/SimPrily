#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <sstream>
#include <stdlib.h>

using namespace std;

int main (int argc, char* argv[]) 
{
	if(argc < 2){
		cerr << "Usage: cat dictionary | " << argv[0] << " queries [field]" << endl;
		return 0;
	}

	int fid;
	if ( argc == 3 ) fid = atoi( argv[2] );
	else fid = 1;

	ifstream file_cmp(argv[1]);
	if(!file_cmp) { cerr << "file could not be opened" << endl; return 0; }
	
	// load source
	set<string> source;
	stringstream ss;
	string line, id;
	while(getline(cin,line))
	{
		ss.clear(); ss.str(line);
		ss >> id;
		source.insert(id);
	}

	while(getline(file_cmp,line))
	{
		ss.clear(); ss.str(line);
		for( int i = 0 ; i < fid ; i++ ) ss >> id;
		if( source.find(id) != source.end() ) cout << line << endl;
	}
	file_cmp.close();
	return 1;
}
