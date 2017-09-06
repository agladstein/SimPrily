#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

const char MIS='0';
const char HET='h';

int main (int argc, char* argv[]) 
{
	string line, discard, fam, id;
	int nr_snp;
	if(argc < 3){
		cerr << "Usage: <ped file> <map file>";
		return 0;
	}
	ifstream file_ped(argv[1]);
	ifstream file_map(argv[2]);
	if(!file_ped || !file_map) { cerr << "file could not be opened" << endl; return 0; }
	
	// load marker names
	vector<string> map;
	while(!file_map.eof())
	{
		discard = line = "";
		file_map >> discard >> line >> discard >> discard;
		if(!file_ped.good() || discard == "" || line == "") continue;
		map.push_back(line);
	}
	nr_snp = map.size();
	cerr << nr_snp << " SNPs" << endl;
	
	// load individuals
	vector<string> sample;
	vector< vector<char> > haplotype[2];
	int ctr = 0;
	while(!file_ped.eof())
	{
		fam = id = discard = "";
		file_ped >> fam >> id >> discard >> discard >> discard >> discard;
		if(fam == "" || id == "" || discard == "") continue;
		getline(file_ped,line);
		sample.push_back(id);
		vector<char> seq[2];
		for(int i=0;i<nr_snp;i++)
		{
			seq[0].push_back(line.at(i*4+1));
			seq[1].push_back(line.at(i*4+3));
		}
		haplotype[0].push_back(seq[0]);
		haplotype[1].push_back(seq[1]);
		ctr++;
	}
	int nr_samples = sample.size();
	cerr << nr_samples << " samples" << endl;
	file_map.close();
	file_ped.close();
	
	// print header
	cout << "# sampleID";
	for(int i=0;i<nr_samples;i++)
	{
		cout << '\t' << sample[i] << '\t' << sample[i];
	}
	// print sequences
	for(int h=0;h<nr_snp;h++)
	{
		cout << endl << "M " << map[h];
		for(int i=0;i<nr_samples;i++)
		{
			cout << '\t' << haplotype[0][i][h] << '\t' << haplotype[1][i][h];
		}
	}
	
	return 1;
}
