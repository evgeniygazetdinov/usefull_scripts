import datetime
from delete_by_time import find_file_date_modification,




def find_filling():

















def test_():
    #write doc and fill up space on hard drive
    import sys
    import errno

    write_str = "!"*1024*1024*5  # 5MB

    output_path = sys.argv[1]

    with open(output_path, "w") as f:
        while True:
            try:
                f.write(write_str)
                f.flush()
            except IOError as err:
                if err.errno == errno.ENOSPC:
                    write_str_len = len(write_str)
                    if write_str_len > 1:
                        write_str = write_str[:write_str_len/2]
                    else:
                        break
                else:
                    raise
