# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name		oro

Name:           jakarta-oro
Version:        2.0.8
Release:        10
Summary:        Full regular expressions API
License:        ASL 1.1
Group:          Development/Java
Source0:        %{name}-%{version}.tar.gz
Source1:        MANIFEST.MF
Patch1:         %{name}-build-xml.patch
URL:            http://jakarta.apache.org/oro
BuildRequires:  jpackage-utils > 1.6
BuildRequires:  ant
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
Provides:       oro = %{version}-%{release}
Obsoletes:      oro <= 0:2.0.8

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
Provides:       oro-javadoc = %{version}-%{release}
Obsoletes:      oro-javadoc <= 0:2.0.8
#BuildRequires:  java-javadoc
# for /bin/rm and /bin/ln
Requires(post):  coreutils
Requires(postun): coreutils

%description javadoc
Javadoc for %{name}.

%prep
rm -rf %{buildroot}
%setup -q -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# remove all CVS files
for dir in `find . -type d -name CVS`; do rm -rf $dir; done
for file in `find . -type f -name .cvsignore`; do rm -rf $file; done

%patch1
cp %{SOURCE1} .

%build
ant -Dfinal.name=%{base_name} jar javadocs

%install
#jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{base_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && ln -sf %{name}-%{version}.jar %{base_name}-%{version}.jar)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
#javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink
rm -rf docs/api

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COMPILE ISSUES README TODO CHANGES CONTRIBUTORS LICENSE STYLE
%{_javadir}/*.jar

%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

