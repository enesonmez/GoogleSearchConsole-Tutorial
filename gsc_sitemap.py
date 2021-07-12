def upload_sitemap(webmasters_service,site,sitemap_list):
    print (f'Uploading sitemaps to {site}')
    for sitemap in sitemap_list:
        feedpath = site + sitemap
        print(feedpath)
        webmasters_service.sitemaps().submit(siteUrl=site, feedpath=feedpath).execute()