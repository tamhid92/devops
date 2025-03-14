import requests
from bs4 import BeautifulSoup
import re

def scrape_by_class(url, class_name):

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        elements = soup.find_all(class_=class_name)

        extracted_data = [element.text.strip() for element in elements]
        return extracted_data

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_full_pkg_name(full_pkg_list, name):
    
    for pkg in full_pkg_list:
        if name == "flit-core":
            name = "flit_core"
        if name == "libelf":
            name = "elfutils"
        pkg_without_ext = re.sub(r".tar.*", "", pkg)
        if name in pkg:
            return pkg, pkg_without_ext
    raise Exception(f"Unable to find package with the name {name}")

if __name__ == "__main__":

    pkg_list = ["acl.html","attr.html","autoconf.html","automake.html","bash.html","bc.html","binutils.html","bison.html","bzip2.html","check.html","coreutils.html","dejagnu.html","diffutils.html","e2fsprogs.html","expat.html","expect.html","file.html","findutils.html","flex.html","flit-core.html","gawk.html","gcc.html","gdbm.html","gettext.html","glibc.html","gmp.html","gperf.html","grep.html","groff.html","grub.html","gzip.html","iana-etc.html","inetutils.html","intltool.html","iproute2.html","jinja2.html","kbd.html","kmod.html","less.html","libcap.html","libelf.html","libffi.html","libpipeline.html","libtool.html","libxcrypt.html","lz4.html","m4.html","make.html","man-db.html","man-pages.html","markupsafe.html","meson.html","mpc.html","mpfr.html","ncurses.html","ninja.html","openssl.html","patch.html","perl.html","pkgconf.html","procps-ng.html","psmisc.html","readline.html","sed.html","setuptools.html","shadow.html","sysklogd.html","sysvinit.html","tar.html","tcl.html","texinfo.html","udev.html","util-linux.html","vim.html","wheel.html","xz.html","zlib.html","zstd.html"]
    print(f"Total packages to be installed: {len(pkg_list)}")
    print(f"TODO MANUALLY: XML-Parser")
    req = requests.get("https://www.linuxfromscratch.org/lfs/view/stable/wget-list-sysv")
    url_list = req.text.split("\n")
    pkgs_list = []

    for pkg_url in url_list:
        if ".patch" in pkg_url:
            pass
        elif pkg_url == "":
            pass
        else:
            pkg = pkg_url.split("/")[-1]
            pkgs_list.append(pkg)


    for pkg in pkg_list:
        url = f"https://www.linuxfromscratch.org/lfs/view/stable/chapter08/{pkg}"
        class_name = "userinput"

        package_name, package_name_no_ext = get_full_pkg_name(pkgs_list, pkg.split(".")[0])
        extracted_content = scrape_by_class(url, class_name)

        unzip_cmd = f"""
tar -xvf {package_name}
cd {package_name_no_ext}
        """

        with open("chapter8.sh", "a+") as file:
            file.write(f"\n##Installing Package {pkg.split(".")[0]}\n")
            file.write(unzip_cmd)

        if extracted_content:
            for item in extracted_content:
                with open("chapter8.sh", "a+") as file:
                    file.write("\n")
                    file.write(item)
        with open("chapter8.sh", "a+") as file:
            file.write("\ncd $LFS/sources")
            file.write(f"\nrm -rf {package_name_no_ext}")