#include <iostream>
#include <openssl/des.h>
#include <fstream>
#include <string>
#include <cstring>
#define ENC 1
#define DEC 0
using namespace std;

#pragma comment(lib, "libeay32.lib") 
#pragma comment(lib, "ssleay32.lib")

int main()
{
    //input��iv key inputfile outputfile
    string ini_iv, ini_key, inputfile, outputfile;
    cin >> ini_iv >> ini_key >> inputfile >> outputfile;

    if (ini_iv.length() != 16) {
        printf("\ninitial iv is wrong!\n");
        return 0;
    }
    if (ini_key.length() != 16) {
        printf("\nkey is wrong!\n");
        return 0;
    }

    //�����ʼ����iv
    //des_longΪunsigned long�ͣ�ռ4���ֽ�
    DES_LONG iv[2];//8λʮ��������Ϊһ��
    iv[0] = stoul(ini_iv.substr(0, 8), nullptr, 16);
    iv[1] = stoul(ini_iv.substr(8, 8), nullptr, 16);
    printf("\ninitial iv is: %lu%lu\n", iv[0], iv[1]);

    //������Կkey
    unsigned char cbc_key[8];
    for (int i = 0; i < 8; i++) {
        cbc_key[i] = stoi(ini_key.substr(0 + 2 * i, 2), nullptr, 16);
    }
    printf("\ninitial key is: 0x%x%x%x%x%x%x%x%x\n",
        cbc_key[0], cbc_key[1], cbc_key[2], cbc_key[3], cbc_key[4], cbc_key[5], cbc_key[6], cbc_key[7]);

    //�õ���Կkey
    int k;
    DES_key_schedule key;
    if ((k = DES_set_key_checked(&cbc_key, &key)) != 0)
        printf("\nkey error\n");


    //���ļ�����,�ļ��ɹ��Ķ�ȡ��buffer��
    ifstream in_file;
    in_file.open(inputfile.c_str(), ios::in | ios::binary);
    in_file.seekg(0, in_file.end);
    int ini_length = in_file.tellg();
    in_file.seekg(0, in_file.beg);
    int length = (ini_length + 7) / 8 * 8;//�����8���ֽڵı���
    char* input_buffer = new char[length];
    memset(input_buffer, 0, sizeof(char) * length);
    in_file.read(input_buffer, length);
    in_file.close();
    DES_LONG* input = (DES_LONG*)input_buffer;
    printf("DES Clear Text: %s\n", input_buffer);

    

    //ѭ������
    DES_LONG iv_p[2];
    iv_p[0] = iv[0];
    iv_p[1] = iv[1];
    for (int i = 0; i < length / 8; i++) {
        input[0 + i * 2] = iv[0] ^ input[0 + i * 2];
        input[1 + i * 2] = iv[1] ^ input[1 + i * 2];
        DES_encrypt1(input + i * 2, &key, ENC);//���ܺ�Ľ���滻ԭ���Ŀ��λ��
        iv[0] = input[0 + i * 2];
        iv[1] = input[1 + i * 2];
    }
    printf("\nEncryption complete!\n");

    //д������
    ofstream out_file;
    out_file.open(outputfile.c_str(), ios::binary);
    out_file.write(input_buffer, length);
    printf("\nOutput complete!\n");

    //��Ŷ����Ľ��ܺ�Ľ��
    iv[0] = iv_p[0];
    iv[1] = iv_p[1];
    for (int i = 0; i < length / 8; i++) {
        iv_p[0] = input[0 + i * 2];
        iv_p[1] = input[1 + i * 2];
        DES_encrypt1(input + i * 2, &key, DEC);
        input[0 + i * 2] = input[0 + i * 2] ^ iv[0];
        input[1 + i * 2] = input[1 + i * 2] ^ iv[1];
        iv[0] = iv_p[0];
        iv[1] = iv_p[1];
    }
    printf("\nDecryption complete!\n");
    printf("\nDES ciphertext is: %s\n", input_buffer);

    return 0;
}
