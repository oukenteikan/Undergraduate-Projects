g++ Function.cpp Manager.cpp User.cpp Mysql.cpp tinystr.cpp tinyxml.cpp tinyxmlerror.cpp tinyxmlparser.cpp -fPIC -shared -o lib.so `mysql_config --cflags --libs`
g++ Main.cpp -o main ./lib.so `mysql_config --cflags --libs`
./main
