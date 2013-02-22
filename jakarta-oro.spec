%define short_name	oro
%define section		free
%define gcj_support	0

Summary:        Full regular expressions API
Name:           jakarta-oro
Epoch:		0
Version:        2.0.8
Release:        3.0.10
License:        Apache License
Group:          Development/Java
Url:            http://jakarta.apache.org/%{name}/
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
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && ln -s %{name}-%{version}.jar %{short_name}-%{version}.jar)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
#javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -s %{name}-%{version} %{name})
(cd %{buildroot}%{_javadocdir} && ln -s %{name}-%{version} %{short_name}-%{version})
(cd %{buildroot}%{_javadocdir} && ln -s %{short_name}-%{version} %{short_name})
rm -rf docs/api

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%doc COMPILE ISSUES README TODO CHANGES CONTRIBUTORS LICENSE STYLE
%{_javadir}/*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}*.jar.*
%endif

%files javadoc
%{_javadocdir}/*

