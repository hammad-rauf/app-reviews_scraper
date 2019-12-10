# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class AppreviewPipeline(object):

    def __init__(self):

        self.create_connection()
        #self.create_table()
        pass

    def create_connection(self):

        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'H@mmad123',
            database = 'appreview'
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):

        self.curr.execute("drop table if exists appreview_table")
        self.curr.execute("CREATE TABLE appreview_table( app_link text,date text,store text,rating text,review text)")
   
    def process_item(self, item, spider):

        self.store_db(item)

        return item

    def store_db(self,item):

        self.curr.execute(f"insert into appreview_table values ('{item['app_link']}','{item['date']}','{item['store']}','{item['rating']}','{item['review']}')")
       
       
        self.conn.commit()
