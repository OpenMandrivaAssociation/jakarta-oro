%define short_name	oro
%define section		free
%define gcj_support	1

Name:           jakarta-oro
Version:        2.0.8
Release:        3.0.10
Epoch:		0
Summary:        Full regular expressions API
License:        Apache License
Group:          Development/Java
URL:            http://jakarta.apache.org/%{name}/
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  java-rpmbuild > 0:1.5
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Provides:       oro = %{epoch}:%{version}-%{release}
#Vendor:         JPackage Project
#Distribution:   JPackage

%description
The Jakarta-ORO Java classes are a set of text-processing Java classes
that provide Perl5 compatible regular expressions, AWK-like regular
expressions, glob expressions, and utility classes for performing
substitutions, splits, filtering filenames, etc. This library is the
successor to the OROMatcher, AwkTools, PerlTools, and TextTools
libraries from ORO, Inc. (www.oroinc.com). They have been donated to the
Jakarta Project by Daniel Savarese (www.savarese.org), the copyright
holder of the ORO libraries. Daniel will continue to participate in
their development under the Jakarta Project.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# remove all CVS files
for dir in `find . -type d -name CVS`; do rm -rf $dir; done
for file in `find . -type f -name .cvsignore`; do rm -rf $file; done

%build
%ant -Dfinal.name=%{name} jar javadocs

%install
#jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && ln -s %{name}-%{version}.jar %{short_name}-%{version}.jar)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
#javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -s %{name}-%{version} %{name})
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -s %{name}-%{version} %{short_name}-%{version})
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -s %{short_name}-%{version} %{short_name})
rm -rf docs/api

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%doc COMPILE ISSUES README TODO CHANGES CONTRIBUTORS LICENSE STYLE
%{_javadir}/*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}*.jar.*
%endif

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/*




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:2.0.8-3.0.7mdv2011.0
+ Revision: 665811
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.0.8-3.0.6mdv2011.0
+ Revision: 606065
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.0.8-3.0.5mdv2010.1
+ Revision: 523009
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:2.0.8-3.0.4mdv2010.0
+ Revision: 425447
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:2.0.8-3.0.3mdv2009.1
+ Revision: 351293
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:2.0.8-3.0.2mdv2009.0
+ Revision: 167953
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:2.0.8-3.0.2mdv2008.1
+ Revision: 120920
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

  + Alexander Kurtakov <akurtakov@mandriva.org>
    - bump release

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.0.8-2.6mdv2008.0
+ Revision: 87419
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:2.0.8-2.5mdv2008.0
+ Revision: 82592
- update to new version


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 2.0.8-2.4mdv2007.1
+ Revision: 143935
- rebuild for 2007.1
- Import jakarta-oro

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:2.0.8-2.3mdv2007.0
- rename to jakarta-oro

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:2.0.8-2.2mdv2006.0
- rebuild for libgcj.so.7
- aot compile

* Sun May 08 2005 David Walluck <david@anti-microsoft.org> 0:2.0.8-2.1mdk
- release

* Wed Aug 25 2004 Fernando Nasser <fnasser.redhat.com> 2.0.8-2jpp
- Rebuild with Ant 1.6.2

