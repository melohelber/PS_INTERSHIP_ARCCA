import pandas as pd
import numpy as np
import wscrapTripAd
import SQL_functions
import psycopg2
import time
from SQL_functions import check_connection

def wscrapTripAd_from_list(event,context):

    conn = check_connection('')

    links = SQL_functions.get_links(conn, 'tripadvisorstoreurls')
    for link in links:
        (link_,) = link
        print(link_)
        url = link_

        filename = ('rvw_' + url[url.find('Reviews-') + 8:url.find('_State_of_')] + '_' + url[url.find('_Review-') + 17:url.find('-Reviews-')]).lower().replace("-", "_")
        exist = SQL_functions.check_exists(check_connection(conn), filename)

        try:
            t0 = time.time()
            if exist == False:
                print('   Creating new table and saving data...')
                [filename_csv, df] = wscrapTripAd.wsp_from_newlink(url)
                SQL_functions.create_table(check_connection(conn), filename)
            else:
                print('   Updating table...')
                rvw_count = int(SQL_functions.get_table_row_count(check_connection(conn), filename))
                if rvw_count > 0:
                    [(last_rvw_ID, last_rvw_date)] = SQL_functions.get_table_last_rvw_date_ID(check_connection(conn), filename)
                    [last_rvw_ID, last_rvw_date] = [int(last_rvw_ID), pd.to_datetime(last_rvw_date, dayfirst=True).date()]

                    [upd_per_count, upd_per_ID, upd_per_date] = [True, False, False]
                    [filename_csv, df] = wscrapTripAd.wsp_update_from_link(url, rvw_count, last_rvw_ID, last_rvw_date, upd_per_count, upd_per_ID, upd_per_date)
                    
                    if filename_csv == 'r_count == rvw_count':
                        print('   Not updated: New r_count == Old rvw_count')

                elif rvw_count == 0:
                    [filename_csv, df] = wscrapTripAd.wsp_from_newlink(url)
            


            print('\n')
            # df['n_reviews'] = df['n_reviews'].fillna(0).astype(int)
            df = df.replace(np.nan, '', regex=True).replace(pd.NaT, '', regex=True).replace("'", "`", regex = True)
            df.fillna('',inplace=True)
            t1 = time.time()
            print('   Delta_t for WebScraping %f minutes\n'%((t1-t0)/60))

            try:
                SQL_functions.insert_all_DF_Data(check_connection(conn), df, filename)
                print('--->Success saved in PostGre for %s\n'%filename)
            except:
                print('--->Unsuccessful save for %s\n'%filename)
        except:
            if filename_csv is False:
                print('--->Error for %s\n'%filename)
            pass

if __name__ == "__main__":
    wscrapTripAd_from_list(None, None)