
#first argument from logs
arrIN=(${1//./ })
FILE_WITHOUT_EXTENSION=${arrIN[0]};
FDB=$"$FILE_WITHOUT_EXTENSION"".FDB";
FBK=$"$FILE_WITHOUT_EXTENSION"".FBK";
printf "\n CONVERTER \n";
printf "\n";
printf "Convert from : %s\n to: %s\n" "$FBK" "$FDB";
printf "\n";
# formating command
MYCOMMAND=$"docker exec -it firebird gbak -user SYSDBA -password masterkey -C /firebird/data/""$FBK"" /firebird/data/""$FDB";
echo $MYCOMMAND;
eval $MYCOMMAND;
