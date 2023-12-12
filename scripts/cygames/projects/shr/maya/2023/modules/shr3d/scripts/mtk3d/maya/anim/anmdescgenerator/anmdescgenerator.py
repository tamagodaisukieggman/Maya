# coding: UTF-8
import csv, codecs

csvPath = 'idlist.csv'
loadCsv = 'filename.csv'
textPath = 'list.txt'

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

#書き込み
def writeTxt(textLists):

    textC = textLists

    tF = open(textPath, mode='w')

    for a in range(len(textC)) :
        tF.write((textC[a]).encode('utf-8'))

    tF.close()

def main():
    #検索用CSVファイル
    with open(loadCsv,'rb') as idListCsvFile:
        idcsv_reader = UnicodeReader(idListCsvFile)
        searchRawIdList = []
        for idName in idcsv_reader :
            searchRawIdList.append(idName[0])

    #拡張子の排除
    searchIdList = []
    for b in searchRawIdList :
        splitExt = b.split(".")
        searchIdList.append(splitExt[0])

    #参照用CSVファイル
    with open(csvPath,'rb') as csvfile:
        csv_reader = UnicodeReader(csvfile)

        charId = []

        """
        for row in csv_reader:
            print(u"csv:" + row[0])
            for ids in range(len(searchIdList)):
                print(u"list： " + searchIdList[ids])
                if searchIdList[ids] == row[0]:
                    print(u"マッチ："+ row[0] + u" 日本語:" + row[1])
                    charString = row[1] + " "
                    charId.append(charString)
                else :
                    print("None")
        """
        csvList = []

        for pu in csv_reader:
            csvList.append(pu)

    #検索と文字列作成
    stringList = []
    charId = []
    for idlist in range(len(searchIdList)):
        sil = searchIdList[idlist].split("_")
        charId.append(searchIdList[idlist])
        charId.append('\t')
        for ids in range(len(sil)):
            for row in csvList:
                #print(u"list： " + sil[ids])
                if sil[ids] == row[0]:
                    charString = row[1] + " "
                    charId.append(charString)
        charId.append('\r\n')
    writeTxt(charId)
